<template>
  <div>
    <b-row>
      <b-col>
        <h1 class="text-center">Register new Account</h1>
      </b-col>
    </b-row>
    <b-row>
      <b-col class="col-xl-4 col-l-4 col-md-6 col-sm-12 mx-auto">
        <b-alert dismissible v-model="hasError" variant="danger">
          {{errorCode}}
        </b-alert>
      </b-col>
    </b-row>
    <b-row>
      <b-col class="col-xl-4 col-l-4 col-md-6 col-sm-12 mx-auto">
        <b-form @submit="submitForm">
          <b-form-group
            description="Enter your virtual street address"
            id="input-group-1"
            label="Email"
            label-for="input-1"
          >
            <b-form-input
              id="input-1"
              placeholder="Email"
              required
              type="email"
              v-model="login.email"
            ></b-form-input>
          </b-form-group>

          <b-form-group description="Choose a secret to guard your identity" id="input-group-2" label="Password"
                        label-for="input-2">
            <b-form-input
              id="input-2"
              placeholder="Password"
              required
              type="password"
              v-model="login.password"
            ></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="success">Register</b-button>
          <b-button @click="loginAccount()" variant="outline-secondary">Login</b-button>
        </b-form>
      </b-col>
    </b-row>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        login: {
          email: '',
          password: '',
        },
        hasError: false,
        errorCode: 'Generic error',
        login_filler: {
          grant_type: '',
          email: '',
          password: '',
          scope: '',
          client_id: '',
          client_secret: ''
        }
      }
    },
    methods: {
      loginAccount() {
        this.$router.push('/login')
      },

      async submitForm(evt) {
        evt.preventDefault()
        try {

          let data = await this.$axios.post('/auth/register', {
            'email': this.login.email,
            'password': this.login.password
          }).catch(
            (error) => {
              this.hasError = true
              this.errorCode = error.response.data.detail
            }
          )

          if (!data.detail) {
            this.$router.push('/login')
          } else {
            this.hasError = true
            this.errorCode = data.detail
          }
        } catch (e) {
          this.$router.push('/register')
        }
      },

      async login(data) {
        this.login_filler.username = data.username;
        this.login_filler.password = data.password;
        try {
          await this.$auth.loginWith('local', {
            data: Object.keys(this.login_filler).map(key => `${key}=${this.login_filler[key]}`).join('&')
            //data:this.login
          })
          this.$router.push('/dashboard')
        } catch (e) {
          this.hasError = true;
          this.errorCode = e.toString();
          //this.$router.push('/login')
        }
      },


      /*async userLogin() {
       try {
         let response = this.$axios.$post('/auth/regster', {data:Object.keys(this.login).map(key => `${key}=${this.login[key]}`).join('&')}
         //let response = this.$auth.loginWith('local', { data: Object.keys(this.login).map(key => `${key}=${this.login[key]}`).join('&') }).then(() => this.$toast.success('Logged In!'))
         console.log(response)
       } catch (err) {
         console.log(err)
       }
     }*/
    }
  }
</script>
