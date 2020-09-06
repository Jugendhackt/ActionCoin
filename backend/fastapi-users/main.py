import os
import time

import motor.motor_asyncio
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi_users import FastAPIUsers, models
from fastapi import Depends
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase

DATABASE_URL = "mongodb://localhost:27017"
#SECRET = str(os.environ.get('ACTIONKEY'))
SECRET = str('ChangeThis')

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(models.BaseUser):
    coins: int = 0

class UserCreate(models.BaseUserCreate):
    pass

class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["actioncoin"]
user_collection = db["users"]
transaction_collection = db["transactions"]
user_db = MongoDBUserDatabase(UserDB, user_collection)


def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
)

fastapi_users = FastAPIUsers(
    user_db, [jwt_authentication], User, UserCreate, UserUpdate, UserDB,
)

app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

#app.include_router(fastapi_users.get_device_router(), prefix="/devices", tags=["devices"])
# app.include_router(devices.create_device(), prefix="/devices", tag=["devices"])
# app.include_router(
#    devices.router,
#    prefix="/devices",
#    tags=["devices"],
#    responses={404: {"description": "Not found"}},
# )

@app.get("/coins")
def get_coins(user: User = Depends(fastapi_users.get_current_user)):
    return {'coins': user.coins}

@app.get("/buy_history")
async def buy_history(user: User = Depends(fastapi_users.get_current_user)):
    transactions = await transaction_collection.find({"target": user.email}).to_list(length=None)
    for transaction in transactions:
        del transaction["_id"]

    return transactions

@app.get("/sell_history")
async def sell_history(user: User = Depends(fastapi_users.get_current_user)):
    transactions = await transaction_collection.find({"source": user.email}).to_list(length=None)
    for transaction in transactions:
        del transaction["_id"]

    return transactions

@app.get("/get_transaction")
async def get_transaction(token: str, user: User = Depends(fastapi_users.get_current_user)):
    transaction = await transaction_collection.find_one({"token": token})
    if transaction == None:
        return {"information": "transaction not found"}

    del transaction["_id"]
    return transaction

@app.post("/create_transaction")
def create_transaction(content: list, user: User = Depends(fastapi_users.get_current_user)):
    token = ''.join(__import__("random").choice(__import__("string").ascii_lowercase) for i in range(4))
    transaction_collection.insert_one({"token": token, "source": user.email, "target": "", "status":"pending", "time": int(time.time()), "content": content})
    return token

@app.post("/accept_transaction")
async def accept_transaction(token: str, user: User = Depends(fastapi_users.get_current_user)):
    transaction = await transaction_collection.find_one({"token": token})

    if transaction == None:
        return {"information": "transaction not found"}

    del transaction["_id"]

    cost = 0
    for content_index in transaction["content"]:
        cost = content_index["amount"] * content_index["cost"]

    if cost > user.coins:
        return {"information": "not enough money"}

    user.coins = user.coins - cost
    # jumk
    trader = await user_collection.find_one({"email": transaction['source']})
    await user_collection.update_one(trader, {"$set": {"coins": trader['coins'] + cost}})
    await user_collection.update_one(user, {"$set": {"coins": user.coins - cost}})

    await transaction_collection.update_one({"token": token}, {"$set": {"status": "done", "target": user.email, "token": "", "time": int(time.time())}})

    return {}

@app.post("/decline_transaction")
def decline_transaction(token: str, user: User = Depends(fastapi_users.get_current_user)):
    transaction_collection.delete_one({"token": token})
