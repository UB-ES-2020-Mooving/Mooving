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
  </div>
</template>

<script>
const home = { lat: 41.417988, lng: 2.185246 };
export default {
  data() {
    return {
      // default to Montreal to keep it simple
      // change this to whatever makes sense
      center: { lat: 45.508, lng: -73.587 },
      markers: [],
      places: [],
      currentPlace: null,
      myCoordinates: {
          lat: 0,
          ln: 0
      }
    };
  },
  mounted() {
    this.geolocate();
  },
  created() {
    this.$getLocation({})
        .then(coordinates => {
          this.myCoordinates = coordinates;
        })
        .catch( error => alert(error));
    this.drawDirection()
  },
  methods: {
    // receives a place object via the autocomplete component
    setPlace(place) {
      this.currentPlace = place;
    },
    drawDirection() {
        this.markers = [
          {
            position: home,
          },
          {
            position: {lat: 41.43, lng: 2.186}
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
