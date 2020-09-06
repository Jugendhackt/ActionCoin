# ActionCoin

## Frontend

### Installation

```shell
> Install NodeJs
> Install NPM
cd frontend
npm install
```

### Run

```shell
npm run dev
```

## Backend

### Installation

```shell
pip install uvicorn
pip install fastapi-users[mongodb]
cd backend/fastapi-users
```

*Alternative approach for Nix/NixOS*

```shell
cd backend/fastapi-users
nix-shell
```
### Run

```shell
python -m uvicorn main:app --reload
```
