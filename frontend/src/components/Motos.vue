<template>
  <div id="app" style="margin-top: 0">
    <!-- Nav bar with the logo of the company -->
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
      <!-- Brand -->
      <a class="navbar-brand" href="#">
        <img src="./Images/moovingLogoBlanco.png" alt= "Logo" style= "width:100px; margin-top: 0">
      </a>
    </nav>
    <!-- Title of the page -->
    <h1> {{ name }} </h1>
    <!-- Lista de motos para el mecanico-->
    <div class="list-group">
      <!-- Mostrar cabecera y lista solo si hay elementos -->
      <div id="lista_motos_mechanic" v-if="displayed_motos.length>0" class="center-screen">
        <div class="row">
          <div class="col-sm">License plate</div>
          <div class="col-sm">State</div>
          <div class="col-sm">Distance (in meters)</div>
          <div class="col-sm">Type</div>
        </div>
        <button v-for="item in displayed_motos" :key="item.license_plate" type="button" class="list-group-item list-group-item-action"  @click="checkMoto()">
          <div class="row">
            <div class="col-sm" style="font-weight: bold;">{{item.license_plate}}</div>
            <div class="col-sm" style="font-weight: bold;">{{item.state}}</div>
            <div class="col-sm">{{item.distance}}</div>
            <div class="col-sm">{{item.type}}</div>
          </div>
        </button>
      </div>
      <!-- Mensaje si no hay motos que el mecanico necesite reparar -->
      <!-- Obs: inicialmente deberia ser displayed_motos.items.length pero al recibir la llamada del axios es sin el items-->
      <div id="no_motos_mechanic" v-if="displayed_motos.length===0" class="center-screen">
        <p>{{message_no_motos_mechanic_to_check}}</p>
      </div>
    </div>
    <!-- Lista de motos para el cliente-->
    <div class="list-group">
      <!-- Mostrar cabecera y lista solo si hay elementos -->
      <div id="lista_motos_client" v-if="available_motos.length>0" class="center-screen">
        <div class="row">
          <div class="col-sm">License plate</div>
          <div class="col-sm">Distance (in meters)</div>
          <div class="col-sm">Type</div>
        </div>
        <button v-for="item in available_motos" :key="item.matricula" type="button" class="list-group-item list-group-item-action"  @click="reserveMoto()">
          <div class="row">
            <div class="col-sm">{{item.matricula}}</div>
            <div class="col-sm">{{item.distance_client}}</div>
            <div class="col-sm">{{item.model_generic}}</div>
          </div>
        </button>
      </div>
      <!-- Mensaje si no hay motos disponibles para que el cliente utilice-->
      <div id="no_motos_client" v-if="available_motos.length===0" class="center-screen">
          <p>{{ message_no_motos_available }}</p>
      </div>
    </div>
  </div>
  <!-- Mostrar la lista de motos -->
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      name: 'Motos',
      logged: true,
      show_moto_list: true,
      // available_motos: { items: [] },
      available_motos: {
        items: []
      },
      displayed_motos: {
        items: [ ]
      },
      message_no_motos_mechanic_to_check: 'No motos to check',
      message_no_motos_available: 'There are no motos available'
    }
  },
  created () {
    this.getAvailableMotos() // Gets the motos that are available for the client to use
    this.getMotosToCheck() // Gets the motos that need to be checked by the mechanic
    this.displayAvailableMotosList()
  },
  methods: {
    reserveMoto () {
      // Nos lleva a otra pagina donde se ve la info especifica de la moto
    },
    checkMoto () {
      // El mecanico accede a una pagina con mas info de la moto
    },
    displayAvailableMotosList () {
      // this.displayed_motos = this.available_motos
      // alert('mostrar longitud')
      // alert(this.displayed_motos.items.length)
    },
    getAvailableMotos () {
      const path = 'http://127.0.0.1:5000/motos'
      axios.get(path)
        .then((res) => {
          this.available_motos = res.data.motos
          // alert(res.data.motos)
          // alert(res.data.motos.length)
          console.log(res.data.motos)
        })
        .catch((error) => {
          console.error(error)
          alert(error)
        })
    },
    displayFilteredMotosList () {
      // this.displayed_motos = this.filtered_motos
    },
    getMotosToCheck () {
      const path = 'http://127.0.0.1:5000/mechanicMotos'
      axios.get(path)
        .then((res) => {
          this.displayed_motos = res.data.motos
          // alert(res.data.motos)
          alert(res.data.motos.length)
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

<style scoped>
  nav {
    border-top: 1px solid black;    /* in place of the word "black", you can use #000000 or rgb(0,0,0) */
    border-bottom: 1px solid black;
    margin: 0;
  }
</style>
