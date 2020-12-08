<template>
  <div>
    <div style="margin-top: 0">
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
            <b-nav-item><router-link :to="{path: '/map', query: { email: this.email } }">Map</router-link></b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <div>
      <GmapMap
          :center="myCoordinates"
          :zoom="12"
          style="height:685px;width:360px;margin:0 auto;"> //height:587px
        <GmapMarker
          :key="item.matricula"
          v-for="item in this.available_motos"
          :position="{lat: item.last_coordinate_latitude, lng: item.last_coordinate_longitude}"
          :icon="{ url: require('./Images/green-dot.png')}"
          :clickable="true"
          @click="reserveMoto(item.id)"> //:icon="{ url: require('./Images/iconNormal.png')}"
        </GmapMarker>
        <GmapMarker v-if="is_moto_reserved"
          :position="{lat: moto_reserved.last_coordinate_latitude, lng: moto_reserved.last_coordinate_longitude}"
          :icon="{ url: require('./Images/purple-dot.png')}"
          :clickable="true"
          @click="center=reserveMoto(moto_reserved.id)">
        </GmapMarker>
        <GmapMarker v-if="is_moto_running"
          :position="{lat: moto_running.last_coordinate_latitude, lng: moto_running.last_coordinate_longitude}"
          :icon="{ url: require('./Images/orange-dot.png')}"
          :clickable="true"
          @click="reserveMoto(moto_running.id)">
        </GmapMarker>
        <GmapMarker
          :position="{lat: myCoordinates.lat, lng: myCoordinates.lng}"
          :icon="{ url: require('./Images/blue-dot.png')}"
          :clickable="true">
        </GmapMarker>
      </GmapMap>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const home = { lat: 41.417988, lng: 2.185246 };
const home2 = { lat: 41.41793, lng: 2.18523 };
export default {
  data() {
    return {
      center: { lat: 45.508, lng: -73.587 },
      places: [],
      currentPlace: null,
      myCoordinates: {
          lat: 0,
          ln: 0
      },
      m: true,
      available_motos: {
        items: []
      },
      model_generic: 'all',
      more_km_restantes: 5,
      moto_running: {
        id: 7,
        matricula: 'ASDJ',
        distance: 0,
        model_generic: 'PATATAS',
        last_coordinate_latitude: 41.417988,
        last_coordinate_longitude: 2.185246
      },
      moto_reserved: {
        id: 1,
        matricula: 'ASD',
        distance: 0,
        model_generic: 'PATATAS',
        last_coordinate_latitude: 41.417983 ,
        last_coordinate_longitude: 2.185244
      },
      is_moto_reserved: false,
      is_moto_running:false
    };
  },
  mounted() {
    this.geolocate();
  },
  created() {
    this.email = this.$route.query.email
    this.$getLocation({})
        .then(coordinates => {
          this.myCoordinates = coordinates;
        })
        .catch( error => alert(error));
    this.getAvailableMotos() // Gets the motos that are available for the client to use
    this.getReservedMoto() // Gets the moto reserved by this user
    this.getRunningMoto() //  Gets the moto that is being run by this user
    this.drawDirection()
  },
  methods: {
    // receives a place object via the autocomplete component
    setPlace(place) {
      this.currentPlace = place;
    },
    reserveMoto (id) {
      // Nos lleva a otra pagina donde se ve la info especifica de la moto
      this.$router.push({ path: '/clientMoto', query: { id: id, email: this.email } })
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
      const path = process.env.VUE_APP_CALL_PATH + '/reserve' + '/' + this.email
      console.log(process.env.VUE_APP_CALL_PATH + '/reserve' + '/' + this.email)
      axios.get(path)
        .then((res) => {
          this.is_moto_reserved = true
          // si hay moto, actualizar moto_reserved
          this.moto_reserved.matricula = res.data.reserved_moto.matricula
          this.moto_reserved.distance = res.data.reserved_moto.distance
          this.moto_reserved.id = res.data.reserved_moto.id
          this.moto_reserved.model_generic = res.data.reserved_moto.model_generic
        })
        .catch((error) => {
          // Si no hay moto reservada, saltara un error
          this.is_moto_reserved = false
          console.error(error)
        })
    },
    getRunningMoto () {
      // Call to the api GET to obtain the running motos by this user
      const path = process.env.VUE_APP_CALL_PATH + '/start' + '/' + this.email
      console.log(process.env.VUE_APP_CALL_PATH + '/start' + '/' + this.email)
      axios.get(path)
        .then((res) => {
          console.log(res.data.reserved_moto)
          this.moto_running.matricula = res.data.start_moto.matricula
          this.moto_running.distance = res.data.start_moto.distance
          this.moto_running.id = res.data.start_moto.id
          this.moto_running.model_generic = res.data.start_moto.model_generic
          this.is_moto_running = true
          // alert('Hay moto runeando!')
        })
        .catch((error) => {
          // No esta runeando ninguna moto
          this.is_moto_running = false
          console.error(error)
          // alert('No hay moto runeando!!!')
        })
    },
    geolocate: function() {
      navigator.geolocation.getCurrentPosition(position => {
        this.center = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
      });
    }
  }
};
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
