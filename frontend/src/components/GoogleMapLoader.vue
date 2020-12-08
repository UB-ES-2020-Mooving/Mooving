<template>
  <div>
    <div>
      <div>
        <h1>Your coordinates:</h1>
        <p> {{ myCoordinates.lat }} Latitude, {{ myCoordinates.lng }} Longitude</p>
      </div>
      <GmapMap
          :center="myCoordinates"
          :zoom="12"
          style="width:640px; height:360px; margin: 32px auto;">
        <GmapMarker
          :key="item.matricula"
          v-for="item in this.available_motos"
          :position="{lat: item.last_coordinate_latitude, lng: item.last_coordinate_longitude}"
          :icon="{ url: require('./Images/green-dot.png')}"
          :clickable="true"
          :draggable="true"
          @click="reserveMoto(item.id)"> //:icon="{ url: require('./Images/iconNormal.png')}"
        </GmapMarker>
        <GmapMarker
          :key="index"
          v-for="(pin, index) in markers2"
          :position="pin.position"
          :icon="{ url: require('./Images/green-dot.png')}"
          :clickable="true"
          :draggable="true"
          @click="center=pin.position">
        </GmapMarker>
        <GmapMarker
          :key="index"
          v-for="(pin, index) in markers3"
          :position="pin.position"
          :icon="{ url: require('./Images/purple-dot.png')}"
          :clickable="true"
          :draggable="true"
          @click="hola">
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
      // default to Montreal to keep it simple
      // change this to whatever makes sense
      center: { lat: 45.508, lng: -73.587 },
      markers: [],
      markers2: [],
      markers3: [],
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
    drawDirection() {
        this.markers = [
          {
            position: home
          }
        ],
        this.markers2 = [
          {
            position: home2,
          },
          {
            position: {lat: 41.432, lng: 2.182}
          }
        ],
        this.markers3 = [
          {
            position: {lat: 41.431, lng: 2.181},
          },
          {
            position: {lat: 41.4325, lng: 2.1825}
          }
        ]
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
h3 {
  margin: 40px 0 0;
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
