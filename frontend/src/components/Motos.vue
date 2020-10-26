<template>
  <div id="app">
    <h1> {{ name }} </h1>
    <!-- Lista de motos -->
    <div class="list-group">
      <!-- Mostrar cabecera y lista solo si hay elementos -->
      <div id="lista_motos" v-if="displayed_motos.items.length>0" class="center-screen">
        <div class="row">
          <div class="col-sm">License plate</div>
          <div class="col-sm">Distance</div>
          <div class="col-sm">Type</div>
        </div>
        <button v-for="item in available_motos.items.sort(function(a, b){return a.distance - b.distance})" :key="item.license_plate" type="button" class="list-group-item list-group-item-action"  @click="reserveMoto()">
          <div class="row">
            <div class="col-sm">{{item.license_plate}}</div>
            <div class="col-sm">{{item.distance}}</div>
            <div class="col-sm">{{item.type}}</div>
          </div>
        </button>
      </div>
        <!-- Mensaje si no hay motos -->
        <div id="no_motos" v-if="available_motos.items.length===0" class="center-screen">
          <p>There are no motos availables</p>
        </div>
    </div>
  </div>
  <!-- Mostrar la lista de motos -->
</template>

<script>
export default {
  data () {
    return {
      name: 'Motos',
      logged: true,
      show_moto_list: true,
      // available_motos: { items: [] },
      available_motos: {
        items: [
          {license_plate: 'apple1', distance: '10', type: 'as', horses: '100'},
          {license_plate: 'apple2', distance: '7', type: 'asdf', horses: '250'},
          {license_plate: 'apple3', distance: '30', type: 'as', horses: '500'},
          {license_plate: 'apple2', distance: '7', type: 'asdf', horses: '250'},
          {license_plate: 'apple3', distance: '23', type: 'as', horses: '500'}
        ]
      },
      displayed_motos: {
        items: []
      }
    }
  },
  created () {
    // this.getAvailableMotos()
    this.displayAvailableMotosList()
  },
  methods: {
    reserveMoto () {
      // Nos lleva a otra pagina donde se ve la info especifica de la moto
    },

    displayAvailableMotosList () {
      this.displayed_motos = this.available_motos
    },
    displayFilteredMotosList () {
      // this.displayed_motos = this.filtered_motos
    }
  }
}
</script>
