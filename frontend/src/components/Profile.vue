<template>
  <div>
    <div>
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
      <div id="prof">
        <div class="col-sm-8">
          <div class="card sm-3">
            <div class="card-body">
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Name</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  {{ this.user.nombre }}
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Email</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  {{ email }}
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">IBAN</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  {{ this.user.iban }}
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">DNI/NIE</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  {{ this.user.dni_nie }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      email: '',
      algo: [],
      user: {
        email: '',
        nombre: '',
        iban: '',
        dni_nie: ''
      }
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
      console.log(process.env.VUE_APP_CALL_PATH + '/profile' + '/' + this.email)
      axios.get(path)
        .then((res) => {
          this.user.nombre = res.data.client_profile.nombre
          this.user.iban = res.data.client_profile.iban
          this.user.dni_nie = res.data.client_profile.dni_nie
          this.user.email = res.data.client_profile.email
        })
        .catch((error) => {
          console.error(error)
          alert(error)
        })
    }
  }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
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
#prof {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  margin-top: 50px;
}
</style>
