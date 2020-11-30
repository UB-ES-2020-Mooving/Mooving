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
    <!-- Lista de motos reservadas -->
    <div id="motosReserved" v-if="is_moto_reserved" style="margin-top: 20px">
      <h2>{{ name_reserved_motos }}</h2>
      <div class="list-group" style="margin-bottom: 20px">
        <div class="center-screen">
          <button type="button" class="list-group-item list-group-item-action" @click="reserveMoto(moto_reserved.id)">
            <div class="row">
              <div class="col-sm" style="font-weight: bold;">{{moto_reserved.matricula}}</div>
              <div class="col-sm">Distance: {{moto_reserved.distance}}m</div>
              <div class="col-sm">Type: {{moto_reserved.model_generic}}</div>
            </div>
          </button>
        </div>
      </div>
      <!-- Show divider between lists-->
      <div class="h-divider" style="margin-bottom: 20px;">
        <!-- div class="text2"><img src="./Images/MotodivisorRightWhite.png" style= "width:100%;"/></div -->
        <hr class="gradient-line" />
      </div>
    </div>
    <!-- Title of the page: Motorbikes for the client -->
    <h2>{{ name }}</h2>
    <!-- Checkboxes to filter moto's type -->
    <h5>Filter type/s of motorbikes: </h5>
    <input type="checkbox" id="checkboxBasic" v-model="basic" @change="filterMotoListByType()">
    <label for="checkboxBasic">Basic </label>
    <input type="checkbox" id="checkboxPremium" v-model="premium" @change="filterMotoListByType()">
    <label for="checkboxPremium">Premium</label>
    <br>
    <!-- Slider to filter moto's remaining km -->
    <h5>Range of remaining battery: </h5>
    <custom-slider :values="sliderValues" v-model="slider_km_restantes" @change=filterMotoListByKmRestantes() />
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
    <!-- Show divider between lists-->
    <div class="h-divider" style="width: 100%;margin-top: 0; height: 7px">
      <div class="text2"><img src="./Images/MotodivisorRightWhite.png" style= "width:90%;height: 100%;"/></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import CustomSlider from 'vue-custom-range-slider'
export default {
  components: {
    CustomSlider
  },
  data () {
    return {
      name: 'Available Motorbikes',
      name_reserved_motos: 'Reserved Motorbike',
      email: '',
      available_motos: {
        items: []
      },
      message_no_motos_available: 'There are no motos available',
      is_client: true,
      basic: true,
      premium: true,
      model_generic: 'all',
      more_km_restantes: 5,
      is_moto_reserved: true,
      moto_reserved: {
        id: 1,
        matricula: 'ASD',
        distance: 0,
        model_generic: 'PATATAS'
      },
      slider_km_restantes: '5',
      sliderValues: [
        {
          label: '50km+',
          value: '50'
        },
        {
          label: '45km',
          value: '45'
        },
        {
          label: '40km',
          value: '40'
        },
        {
          label: '35km',
          value: '35'
        },
        {
          label: '30km',
          value: '30'
        },
        {
          label: '25km',
          value: '25'
        },
        {
          label: '20km',
          value: '20'
        },
        {
          label: '15km',
          value: '15'
        },
        {
          label: '10km',
          value: '10'
        },
        {
          label: '5km',
          value: '5'
        }
      ]
    }
  },
  created () {
    this.getAvailableMotos() // Gets the motos that are available for the client to use
    this.getReservedMoto() // Gets the moto reserved by this user
    this.email = this.$route.query.email // si la extension es @mooving.com es un mecanico
  },
  methods: {
    reserveMoto (id) {
      // Nos lleva a otra pagina donde se ve la info especifica de la moto
      this.$router.push({ path: '/clientMoto', query: { id: id, email: this.email } })
    },
    filterMotoListByType () {
      if (this.basic && this.premium) {
        this.model_generic = 'all'
      } else if (this.basic) {
        this.model_generic = 'basic'
      } else if (this.premium) {
        this.model_generic = 'premium'
      } else {
        this.model_generic = 'all'
      }
      this.getAvailableMotos()
    },
    filterMotoListByKmRestantes () {
      this.more_km_restantes = parseInt(this.slider_km_restantes, 10)
      this.getAvailableMotos()
    },
    getAvailableMotos () {
      const path = process.env.VUE_APP_CALL_PATH + '/motos'
      axios.get(path, {
        params: {
          model_generic: this.model_generic,
          more_km_restantes: this.more_km_restantes
        }
      })
        .then((res) => {
          this.available_motos = res.data.motos
          console.log(res.data.motos)
        })
        .catch((error) => {
          console.error(error)
          alert(error)
        })
    },
    getReservedMoto () {
      // Call to the api GET to obtain the reserved motos
      // is_moto_reserved true si hay
      // si hay moto, actualizar moto_reserved
      // si no, revisar que no pete
      this.is_moto_reserved = true
      // alert('Si hay motos reservadas')
    }
  }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2, h3 {
    font-weight: normal;
    text-align: center;
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
  .h-divider {
    margin: auto;
    margin-top: 40px;
    width: 90%;
    position: relative;
    background: #343a40;
  }
  .h-divider .text2 {
    background: #343a40;
  }
  .gradient-line{
    margin: 0 0 0 0;
    display: block;
    border: none;
    height: 10px;
    background: #0071B9;
    background: linear-gradient(to right, #42b983, #343a40, #343a40, #343a40, #42b983);
  }
</style>

