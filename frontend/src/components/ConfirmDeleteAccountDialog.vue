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
                  <input type="password" v-model="user.password" id="password" name="password" class="form-control" :class="{ 'is-invalid': submitted && $v.user.password.$error }" />
                  <div v-if="submitted && $v.user.password.$error" class="invalid-feedback">
                    <span v-if="!$v.user.password.required">Password is required</span>
                    <span v-if="!$v.user.password.minLength">Password must be at least 6 characters</span>
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
      submitted: false
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
        email: this.email,
        password: this.user.password
      }
      // API call
      console.log('API call')
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
