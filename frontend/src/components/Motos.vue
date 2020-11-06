<template>
  <div id="app">
    <h1> {{ name }} </h1>
    <!-- Lista de motos -->
    <div class="list-group">
      <!-- Mostrar cabecera y lista solo si hay elementos -->
      <div id="lista_motos" v-if="available_motos.length>0" class="center-screen">
        <div class="row">
          <div class="col-sm">License plate</div>
          <div class="col-sm">Distance</div>
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
        <!-- Mensaje si no hay motos -->
        <div id="no_motos" v-if="available_motos.length===0" class="center-screen">
          <p>There are no motos availables</p>
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
        items: []
      }
    }
  },
  created () {
    this.getAvailableMotos()
    this.displayAvailableMotosList()
  },
  methods: {
    reserveMoto () {
      // Nos lleva a otra pagina donde se ve la info especifica de la moto
    },

    displayAvailableMotosList () {
      this.displayed_motos = this.available_motos
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
    }
  }
}
</script>
