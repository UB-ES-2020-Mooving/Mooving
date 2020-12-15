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
              <h2>Modify Profile</h2>
              <p> Modify your account detail,<strong> save to confirm</strong>.</p>
              <form @submit.prevent="handleSubmit">
                <div class="form-group">
                  <label for="completeName">Name</label>
                  <input type="text" v-model="user.completeName" id="completeName" name="CompleteName" class="form-control" :class="{ 'is-invalid': submitted && $v.user.completeName.$error }"/>
                  <div v-if="submitted && !$v.user.completeName.required" class="invalid-feedback">Name is required</div>
                </div>
                <div class="form-group">
                  <label for="email">Email</label>
                  <input type="email" v-model="user.email" id="email" name="email" class="form-control" :class="{ 'is-invalid': submitted && $v.user.email.$error || error_email}" />
                  <div v-if="submitted && $v.user.email.$error" class="invalid-feedback">
                    <span v-if="!$v.user.email.required">Email is required</span>
                    <span v-if="!$v.user.email.email">Email is invalid</span>
                  </div>
                  <div v-if="error_email" style="margin-top: 20px;margin-bottom: 20px;">
                    <p style="color: red; font-size: 12px">It seems that a user with that email already exists.</p>
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
                  <label for="dniNie">DNI/NIE</label>
                  <input type="text" v-model="user.dniNie" id="dniNie" name="dniNie" class="form-control" :class="{ 'is-invalid': submitted && $v.user.dniNie.$error || error_dniNie}" />
                  <div v-if="submitted && $v.user.dniNie.$error" class="invalid-feedback">
                    <span v-if="!$v.user.dniNie.required">DNI/NIE is required</span>
                    <span v-if="!$v.user.dniNie.minLength">DNI/NIE must be at least 8 characters</span>
                  </div>
                  <div v-if="error_dniNie" style="margin-top: 20px;margin-bottom: 20px;">
                    <p style="color: red; font-size: 12px">It seems that a user with that DNI/NIE already exists.</p>
                  </div>
                </div>
                <div class="form-row flex-nowrap" style="margin-top: 20px;margin-bottom: 20px; margin-left: 16px; margin-right: 15px">
                  <button class="btn"
                    id="cancelModifyAccount"
                    type="button"
                    @click="cancelModifyAccount()"
                    style="border-radius: 12px;
                    background-color: #ff6961;color: #ffffff; width: 150px
                    margin-left: 0px; margin-right: 10px">
                    Cancel
                  </button>
                  <button class="btn "
                    style="border-radius: 12px;
                    background-color: #343a40;color: #42b983; width: 150px;
                    margin-right: 0px; margin-left: 18px">
                    Save
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
import { required, email, minLength, maxLength, sameAs } from 'vuelidate/lib/validators'
import axios from 'axios'

export default {
  data () {
    return {
      user: {
        completeName: '',
        dniNie: '',
        iban: '',
        email: ''
      },
      submitted: false,
      error_dniNie: false,
      error_email: false
    }
  },
  validations: {
    user: {
      completeName: { required },
      dniNie: { required, minLength: minLength(8) },
      iban: { required, minLength: minLength(5), maxLength: maxLength(34) },
      email: { required, email }
    }
  },
  created () {
    this.email = this.$route.query.email
    this.getProfileInfo()
  },
  methods: {
    getProfileInfo () {
      const parameters = {
        email: this.email
      }
      const path = process.env.VUE_APP_CALL_PATH + '/profile' + '/' + this.email
      axios.get(path)
        .then((res) => {
          this.user.completeName = res.data.client_profile.nombre
          this.user.iban = res.data.client_profile.iban
          this.user.dniNie = res.data.client_profile.dni_nie
          this.user.email = res.data.client_profile.email
        })
        .catch((error) => {
          console.error(error)
          alert(error)
        })
    },
    cancelModifyAccount () {
      this.$router.push({ path: '/profile', query: { email: this.email } })
    },
    handleSubmit (e) {
      console.log('patatita')
      this.submitted = true

      // stop here if form is invalid
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }

      const parameters = {
        name: this.user.completeName,
        iban: this.user.iban,
        dni_nie: this.user.dniNie,
        email: this.user.email
      }
      const path = process.env.VUE_APP_CALL_PATH + '/profile/' + this.email
      this.error_dniNie = false
      this.error_email = false
      axios.put(path, parameters)
        .then((res) => {
          this.$router.push({ path: '/profile', query: { email: this.user.email } })
        })
        .catch((error) => {
          console.error(error)
          switch (error.response.status) {
            case 406:
              this.error_dniNie = true
              break
            case 405:
              this.error_email = true
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
