<template>
  <div id="wholePage">
    <b-navbar toggleable type="dark" variant="dark">
        <b-navbar-brand href="#">
          <img src="./Images/moovingLogoBlanco.png" alt= "Logo" style= "width:100px;">
        </b-navbar-brand>

        <b-navbar-toggle target="navbar-toggle-collapse">
          <template #default="{ expanded }">
            <b-icon v-if="expanded" icon="chevron-bar-up"></b-icon>
            <b-icon v-else icon="chevron-bar-down"></b-icon>
          </template>
        </b-navbar-toggle>

        <b-collapse id="navbar-toggle-collapse" is-nav>
          <b-navbar-nav class="ml-auto">
            <b-nav-item v-if="!this.email.includes('@mooving.com')"><router-link :to="{path: '/motospageclient', query: { email: email } }">Motorbikes</router-link></b-nav-item>
            <b-nav-item v-if="this.email.includes('@mooving.com')"><router-link :to="{path: '/motospagemechanic', query: { email: email } }">Motorbikes</router-link></b-nav-item>
            <b-nav-item><router-link :to="{path: '/profile', query: { email: email } }">Personal Info</router-link></b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    <div class="jumbotron">
      <div class="container">
        <div class="row">
          <div class="col-sm-8 offset-sm-2">
            <div>
              <h2>Confirmation</h2>
              <p>Please, re-enter your password to confirm that you want to <strong>delete your account</strong>.</p>
              <form @submit.prevent="handleSubmit">
                <div class="form-group">
                  <label for="password">Password</label>
                  <input type="password" v-model="user.password" id="password" name="password" class="form-control" :class="{ 'is-invalid': submitted && $v.user.password.$error || error_password}" />
                  <div v-if="submitted && $v.user.password.$error" class="invalid-feedback">
                    <span v-if="!$v.user.password.required">Password is required</span>
                    <span v-if="!$v.user.password.minLength">Password must be at least 6 characters</span>
                  </div>
                  <div v-if="error_password" style="margin-top: 20px;margin-bottom: 20px;">
                    <p style="color: red; font-size: 12px">The password is not correct.</p>
                  </div>
                </div>
                <div class="form-group">
                  <button class="btn "
                    style="border-radius: 12px;
                    background-color: #ff6961;color: #ffffff; width: 150px">
                    Confirm
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { required, minLength } from 'vuelidate/lib/validators'
import axios from 'axios'

export default {
  data () {
    return {
      user: {
        password: ''
      },
      submitted: false,
      error_password: false
    }
  },
  validations: {
    user: {
      password: { required, minLength: minLength(6) }
    }
  },
  created () {
    this.email = this.$route.query.email
  },
  methods: {
    handleSubmit (e) {
      console.log('patatita')
      this.submitted = true

      // stop here if form is invalid
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }

      const parameters = {
        password: this.user.password
      }
      // API call
      const path = process.env.VUE_APP_CALL_PATH + '/client/' + this.email
      axios.delete(path, { data: parameters })
        .then((res) => {
          // route to reloaded motorbike info page:
          console.log('EXITO')
          this.$router.push({ path: '/' })
        })
        .catch((error) => {
          console.error(error)
          switch (error.response.status) {
            case 400:
              this.error_password = true
              break
            case 401:
              alert('You cannnot delete an account with a motorbike reserved/running!')
              break
            case 404:
              alert(`It seems that an account with the email ${this.email} doesn't exist.`)
              break
            default:
              alert('Internal Server error, try again or get in touch with customer support')
              break
          }
        })
    }
  }
}
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
#wholePage
  {
  position:fixed;
  padding:0;
  margin:0;

  top:0;
  left:0;

  width: 100%;
  height: 100%;

  background-color: #e9ecef;
  }
</style>
