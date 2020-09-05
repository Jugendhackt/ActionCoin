<template>
  <div>
    <b-row>
      <b-col>
        <h1 class="text-center">Login</h1>
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
            id="input-group-1"
            label="Email"
            label-for="input-1">
            <b-form-input
              id="input-1"
              placeholder="Email"
              required
              type="email"
              v-model="login.username"
            ></b-form-input>
          </b-form-group>
          <b-form-group id="input-group-2" label="Password" label-for="input-2">
            <b-form-input
              id="input-2"
              placeholder="Password"
              required
              type="password"
              v-model="login.password"
            ></b-form-input>
          </b-form-group>
          <b-button @click="submitForm()" type="submit" variant="success">Login</b-button>
          <b-button @click="registerAccount()" variant="outline-secondary">Register</b-button>
        </b-form>
      </b-col>
    </b-row>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        hasError: false,
        errorCode: 'Generic error',
        login: {
          grant_type: '',
          username: '',
          password: '',
          scope: '',
          client_id: '',
          client_secret: ''
        }
      }
    },
    methods: {
      registerAccount() {
        this.$router.push('/register')
      },
      async submitForm(evt) {
        try {
          evt.preventDefault()
        } catch (e) {

        } finally {

        }
        try {
          await this.$auth.loginWith('local', {
            data: Object.keys(this.login).map(key => `${key}=${encodeURIComponent(this.login[key])}`).join('&')
            //data:this.login
          })
          this.$router.push('/dashboard')
        } catch (e) {
          this.hasError = true;
          this.errorCode = e.toString();
          //this.$router.push('/login')
        }
      },

      async userLogin() {
        try {
          let response = this.$auth.loginWith('local', {data: Object.keys(this.login).map(key => `${key}=${this.login[key]}`).join('&')}).then(() => this.$toast.success('Logged In!'))
          console.log(response)
        } catch (err) {
          console.log(err)
        }
      }
    }
  }
</script>
