<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between ">
      <div>
        <h1>Your coordinates:</h1>
        <p> {{ myCoordinates.lat }} Latitude, {{ myCoordinates.lng }} Longitude</p>
      </div>
      <div>
        <h1>Map coordinates:</h1>
        <p> {{ mapCoordinates.lat }} Latitude, {{ mapCoordinates.lng }} Longitude</p>
      </div>
    </div>
    <GmapMap
      :center = "myCoordinates"
      :zoom = "7"
      style="width:640px; height:360px; margin: 32px auto;"
      ref="mapRef">
      <GmapMarker
          :key="index"
          v-for="(pin, index) in markers"
          :position="pin.position"
          :icon="pin.icon"
          :clickable="true"
          :draggable="true"
          @click="center=pin.position">
        </GmapMarker>
    </GmapMap>
  </div>
</template>

<script>
const home = { lat: 41.417988, lng: 2.185246 };
  export default {
    data () {
      return {
        markers: [],
        map: null,
        myCoordinates: {
          lat: 0,
          ln: 0
        }
      }
    },
    created() {
      //user's coordinates
      //npm install --save-dev vue-browser-geolocation
      //npm install --save-dev vue2-google-maps
      this.$getLocation({})
        .then(coordinates => {
          this.myCoordinates = coordinates;
        })
        .catch( error => alert(error));
      this.drawDirection()
    },
    mounted() {
      //add the map to a data object
      this.$refs.mapRef.$mapPromise.then(map => this.map = map);
    },
    methods: {
      drawDirection() {
        this.markers = [
          {
            position: home,
          }
        ]
      }
    },
    computed: {
      mapCoordinates() {
        if(!this.map) {
          return{
            lat: 0,
            lng: 0
          };
        }
        return {
          lat: this.map.getCenter().lat().toFixed(4),
          lng: this.map.getCenter().lng().toFixed(4)
        }
      }
    }
  }
</script>

<style scoped>

</style>