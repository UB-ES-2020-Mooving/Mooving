<template>
  <div class="jumbotron">
    <div class="container">
      <div class="row">
        <div class="col-sm-8 offset-sm-2">
          <div>
            <h2>Log in</h2>
            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                <label for="email">Email</label>
                <input type="email" v-model="user.email" id="email" name="email" class="form-control" :class="{ 'is-invalid': submitted && $v.user.email.$error }" />
                <div v-if="submitted && $v.user.email.$error" class="invalid-feedback">
                  <span v-if="!$v.user.email.required">Email is required</span>
                  <span v-if="!$v.user.email.email">Email is invalid</span>
                </div>
              </div>
              <div class="form-group">
                <label for="password">Password</label>
                <input type="password" v-model="user.password" id="password" name="password" class="form-control" :class="{ 'is-invalid': submitted && $v.user.password.$error }" />
                <div v-if="submitted && $v.user.password.$error" class="invalid-feedback">
                  <span v-if="!$v.user.password.required">Password is required</span>
                  <span v-if="!$v.user.password.minLength">Password must be at least 6 characters</span>
                </div>
              </div>
              <div class="form-group">
                <button class="btn btn-primary">Log in</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { required, email, minLength } from 'vuelidate/lib/validators'
import axios from 'axios'

export default {
  name: 'Login',
  data () {
    return {
      user: {
        email: '',
        password: ''
      },
      submitted: false
    }
  },
  validations: {
    user: {
      email: { required, email },
      password: { required, minLength: minLength(6) }
    }
  },
  methods: {
    handleSubmit (e) {
      this.submitted = true

      // stop here if form is invalid
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }

      const parameters = {
        email: this.user.email,
        password: this.user.password
      }
      console.log('variable')
      console.log(process.env.VUE_APP_CALL_PATH)
      const path = process.env.VUE_APP_CALL_PATH + '/login'
      axios.post(path, parameters)
        .then((res) => {
          if (res.data.type === 'client') {
            this.$router.push({ path: '/motospageclient', query: { email: res.data.client.email } })
          } else {
            // if (this.email.includes('@mooving.com')) { // si la extension es @mooving.com es un mecanico
            this.$router.push({ path: '/motospage', query: { email: res.data.mechanic.email } })
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          alert('email or password incorrect')
        })
    }
  }
}
</script>

<style scoped>

</style>
