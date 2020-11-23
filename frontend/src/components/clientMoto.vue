<template>
  <div>
    <div>
      <b-navbar toggleable type="dark" variant="dark">
        <b-navbar-brand href="#">
          <img src="./Images/moovingLogoBlanco.png" alt= "Logo" style= "width:100px;">
        </b-navbar-brand>
        <b-collapse id="navbar-toggle-collapse" is-nav>
          <b-navbar-nav class="ml-auto">
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
      <div class="row text-center" style="margin-top: 20px;">
        <div class="col-sm-6 sm-4">
          <img class="rounded z-depth-2" alt="100x200" src="./Images/iconPremium.png"
               data-holder-rendered="true" v-if="this.moto.model_generic === 'premium'">
          <img class="rounded z-depth-2" alt="100x200" src="./Images/iconNormal.png"
               data-holder-rendered="true" v-else-if="this.moto.model_generic === 'basic'">
        </div>
      </div>
      <div id="prof" style="margin-top: 20px;">
        <div class="col-sm-8">
          <div class="card sm-3">
            <div class="card-body">
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0"><strong>License Plate</strong></h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  <strong>{{ this.moto.matricula }}</strong>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Distance</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  {{ this.moto.distance }}
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Type</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  {{ this.moto.model_generic }}
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Fuel/Battery</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  {{ this.moto.km_restantes }} km
                </div>
                </div>
                <hr>
                <div class="row">
                  <div class="col-sm-3">
                    <h6 class="mb-0">Street<b-icon icon="geo-alt-fill"></b-icon></h6>
                  </div>
                  <div class="col-sm-9 text-secondary">
                    {{ this.moto.address }}
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
      id: 0,
      moto: {
        matricula: '',
        model_generic: '',
        km_restantes: 0.0,
        address: '',
        distance: 0
      }
    }
  },
  created () {
    this.email = this.$route.query.email
    this.id = this.$route.query.id
    this.getMotoInfo()
  },
  methods: {
    getMotoInfo () {
      const path = process.env.VUE_APP_CALL_PATH + '/clientMoto' + '/' + this.id
      console.log(process.env.VUE_APP_CALL_PATH + '/clientMoto' + '/' + this.id)
      axios.get(path)
        .then((res) => {
          this.moto.matricula = res.data.client_moto.matricula
          this.moto.model_generic = res.data.client_moto.model_generic
          this.moto.km_restantes = res.data.client_moto.km_restantes
          this.moto.address = res.data.client_moto.address
          this.moto.distance = res.data.client_moto.distance
          console.log(res.data.client_moto)
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
