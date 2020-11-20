<template>
  <div class="jumbotron">
    <div class="container">
      <div class="row">
        <div class="col-sm-8 offset-sm-2">
          <div>
            <h2>Register Form</h2>
            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                <label for="completeName">Complete Name</label>
                <input type="text" v-model="user.completeName" id="completeName" name="CompleteName" class="form-control" :class="{ 'is-invalid': submitted && $v.user.completeName.$error }" />
                <div v-if="submitted && !$v.user.completeName.required" class="invalid-feedback">Complete Name is required</div>
              </div>
              <div class="form-group">
                <label for="dniNie">DNI/NIE</label>
                <input type="text" v-model="user.dniNie" id="dniNie" name="dniNie" class="form-control" :class="{ 'is-invalid': submitted && $v.user.dniNie.$error }" />
                <div v-if="submitted && $v.user.dniNie.$error" class="invalid-feedback">
                  <span v-if="!$v.user.dniNie.required">DNI/NIE is required</span>
                  <span v-if="!$v.user.dniNie.minLength">DNI/NIE must be at least 8 characters</span>
                </div>
              </div>
              <div class="form-group">
                <label for="iban">IBAN</label>
                <input type="text" v-model="user.iban" id="iban" name="iban" class="form-control" :class="{ 'is-invalid': submitted && $v.user.iban.$error }" />
                <div v-if="submitted && $v.user.iban.$error" class="invalid-feedback">
                  <span v-if="!$v.user.iban.required">IBAN is required</span>
                  <span v-if="!$v.user.iban.minLength">IBAN must be at least 5 characters</span>
                  <span v-if="!$v.user.iban.maxLength">IBAN must be no more than 34 characters</span>
                </div>
              </div>
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
                <label for="confirmPassword">Confirm Password</label>
                <input type="password" v-model="user.confirmPassword" id="confirmPassword" name="confirmPassword" class="form-control" :class="{ 'is-invalid': submitted && $v.user.confirmPassword.$error }" />
                <div v-if="submitted && $v.user.confirmPassword.$error" class="invalid-feedback">
                  <span v-if="!$v.user.confirmPassword.required">Confirm Password is required</span>
                  <span v-else-if="!$v.user.confirmPassword.sameAsPassword">Passwords must match</span>
                </div>
              </div>
              <div class="form-group">
                <button class="btn btn-primary">Register</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { required, email, minLength, maxLength, sameAs } from 'vuelidate/lib/validators'
import axios from 'axios'

export default {
  name: 'Registration',
  data () {
    return {
      user: {
        completeName: '',
        dniNie: '',
        iban: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      submitted: false
    }
  },
  validations: {
    user: {
      completeName: { required },
      dniNie: { required, minLength: minLength(8) },
      iban: { required, minLength: minLength(5), maxLength: maxLength(34) },
      email: { required, email },
      password: { required, minLength: minLength(6) },
      confirmPassword: { required, sameAsPassword: sameAs('password') }
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
        nombre: this.user.completeName,
        email: this.user.email,
        iban: this.user.iban,
        dni_nie: this.user.dniNie,
        password: this.user.password
      }
      const path = process.env.VUE_APP_CALL_PATH + '/client'
      axios.post(path, parameters)
        .then((res) => {
          alert('User created on success')
          // this.$router.replace({name: 'Motos'})
          this.$router.push({ path: '/motospageclient', query: { email: this.user.email } })
        })
        .catch((error) => {
          console.error(error)
          alert('A user with the same email or DNI/NIE already exists.')
        })
    }
  }
}
</script>

<style scoped>

</style>
