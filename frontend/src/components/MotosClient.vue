<template>
  <div id="app" style="margin-top: 0">
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
            <b-nav-item><router-link :to="{path: '/motospageclient', query: { email: this.email } }">Motorbikes</router-link></b-nav-item>
            <b-nav-item><router-link :to="{path: '/profile', query: { email: this.email } }">Personal Info</router-link></b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <!-- Title of the page -->
    <h1> {{ name }} </h1>
    <!-- Lista de motos para el cliente-->
    <div class="list-group" v-if="is_client">
      <!-- Mostrar cabecera y lista solo si hay elementos -->
      <div id="lista_motos_client" v-if="available_motos.length>0" class="center-screen">
        <button v-for="item in available_motos" :key="item.matricula" type="button" class="list-group-item list-group-item-action"  @click="reserveMoto(item.id)">
          <div class="row">
            <div class="col-sm" style="font-weight: bold;">{{item.matricula}}</div>
            <div class="col-sm">Distance: {{item.distance}}m</div>
            <div class="col-sm">Type: {{item.model_generic}}</div>
          </div>
        </button>
      </div>
      <!-- Mensaje si no hay motos disponibles para que el cliente utilice-->
      <div id="no_motos_client" v-if="available_motos.length===0" class="center-screen">
        <p>{{ message_no_motos_available }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      name: 'Available Motorbikes',
      email: '',
      available_motos: {
        items: []
      },
      message_no_motos_available: 'There are no motos available',
      is_client: true
    }
  },
  created () {
    this.getAvailableMotos() // Gets the motos that are available for the client to use
    this.email = this.$route.query.email // si la extension es @mooving.com es un mecanico
  },
  methods: {
    reserveMoto (id) {
      // Nos lleva a otra pagina donde se ve la info especifica de la moto
      this.$router.push({ path: '/clientMoto', query: { id: id ,email: this.email } })
    },
    getAvailableMotos () {
      const path = process.env.VUE_APP_CALL_PATH + '/motos'
      axios.get(path)
        .then((res) => {
          this.available_motos = res.data.motos
          console.log(res.data.motos)
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
</style>

