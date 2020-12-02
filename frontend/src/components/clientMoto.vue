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
                  {{ this.moto.distance }} m
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
      <!-- final del id prof -->
      <!-- boton para reservar -->
      <div>
        <button class="btn"
                id="reserveButton"
                v-if="!is_reserved"
                :disabled=!can_reserve
                type="button"
                @click="reserveMoto()"
                style="margin-top: 20px;margin-left: 20px;border-radius: 12px;
                background-color: #343a40;color: #42b983;width: 150px">
          Reserve
        </button>
      </div>
      <!-- mensaje de hasta que hora puede recogerla-->
      <div v-if="is_reserved" style="margin-top: 20px;margin-bottom: 20px; margin-left: 20px">
        <p style="font-weight: bold;">{{this.time_pick_up}}</p>
      </div>
      <!-- divisor de opciones-->
      <div class="row" style="margin-top: 20px;margin-bottom: 20px">
        <div style="position: absolute; left: 20px">
          <!-- boton para cancelar la reserva -->
          <button class="btn"
                  id="cancelButton"
                  v-if="is_reserved"
                  type="button"
                  @click="cancelReserve()"
                  style="border-radius: 12px;
                background-color: #ff6961;color: #ffffff; width: 150px">
            Cancel
          </button>
        </div>
        <div style="position: absolute; right: 20px">
          <!-- boton para aceptar la reserva -->
          <button class="btn"
                  id="startButton"
                  v-if="is_reserved"
                  type="button"
                  style="border-radius: 12px;
                background-color: #343a40;color: #42b983; width: 150px" >
            Start
          </button>
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
      },
      is_reserved: false,
      is_running_another_moto: false, // if client is running a moto
      is_another_moto_reserved: false, // if another moto is reserved
      can_reserve: true, // client can reserve a moto
      time_pick_up: 'You have until XX:XX to pick up the motorbike',
      cancel_message: '',
      moto_reserved: {
        matricula: ''
      },
      moto_running: {
        matricula: ''
      }
    }
  },
  created () {
    this.email = this.$route.query.email
    this.id = this.$route.query.id
    this.getMotoInfo()
    this.getReservedMoto() // Gets the moto reserved by this user
    this.getRunningMoto() // Gets the moto running by this user
    // Si no está runeando otra moto y no está reservando otra moto, puede reservarla
    if (!this.is_running_another_moto && !this.is_another_moto_reserved) {
      this.can_reserve = true
      // alert('puede reservar')
      // alert(!this.is_running_another_moto && !this.is_another_moto_reserved)
    } else {
      this.can_reserve = false
      // alert('No puede reservar')
    }
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
    },
    reserveMoto () {
      // Client reserves a moto
      // Llamada a la api método POST para poner la moto a reservada
      //  reserve/string:client_email/int:moto_id
      const parameters = {
        client_email: this.email,
        moto_id: this.id
      }
      // alert(this.email)
      // alert(this.id)
      const path = process.env.VUE_APP_CALL_PATH + '/reserve'
      // console.log(process.env.VUE_APP_CALL_PATH + '/reserve')
      axios.post(path, parameters)
        .then((res) => {
          this.is_reserved = true // Se cambia la visibilidad de los botones
          this.time_pick_up = res.data.message // update the visibility of the message this.time_pick_up
          // alert('Motorbike reserved on success')
          // alert('Reserved was clicked! We will call to the API and the state will change to reserved')
        })
        .catch((error) => {
          console.error(error)
          // alert(error)
          // alert('Motorbike not reserved')
        })
    },
    cancelReserve () {
      // Client cancel the reserve
      // Llamada a la api para poner la moto en available
      // Se cambia la visibilidad de los botones
      const path = process.env.VUE_APP_CALL_PATH + '/reserve' + '/' + this.email + '/' + this.id
      axios.delete(path)
        .then((res) => {
          this.is_reserved = false // Se cambia la visibilidad de los botones
          this.cancel_message = res.data.message
          alert('Until the next rodeo, cowboy!')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getReservedMoto () {
      // Call to the api GET to obtain the reserved motos
      const path = process.env.VUE_APP_CALL_PATH + '/reserve' + '/' + this.email
      console.log(process.env.VUE_APP_CALL_PATH + '/reserve' + '/' + this.email)
      axios.get(path)
        .then((res) => {
          // alert('Obtenidas las motos reservadas')
          // alert('La moto reservada tiene matricula')
          // alert(res.data.reserved_moto.matricula)
          console.log(res.data.reserved_moto)
          this.moto_reserved.matricula = res.data.reserved_moto.matricula
          // Si la moto reservada es la misma
          if (this.moto_reserved.matricula === this.moto.matricula) {
            this.is_another_moto_reserved = false
            this.is_reserved = true
            this.time_pick_up = res.data.message
          }
          // Aqui tenemos una moto reservada, entonces, si son diferentes, no debe poder reservarla
          if (this.moto_reserved.matricula !== this.moto.matricula) {
            // alert('la matricula de la moto reservada es diferente')
            this.can_reserve = false
            // alert('can reserve false')
            // alert(this.moto_reserved.matricula)
            this.is_another_moto_reserved = true
          }
        })
        .catch((error) => {
          // Si no hay moto reservada, saltara un error
          this.is_another_moto_reserved = false
          console.error(error)
          // alert(error.response.status)
        })
    },
    getRunningMoto () {
      // Call to the api GET to obtain the running motos by this user
      const path = process.env.VUE_APP_CALL_PATH + '/start' + '/' + this.email
      console.log(process.env.VUE_APP_CALL_PATH + '/start' + '/' + this.email)
      axios.get(path)
        .then((res) => {
          console.log(res.data.reserved_moto)
          this.moto_running.matricula = res.data.reserved_moto.matricula
          // si esta runeando la misma matricula
          if (this.moto_running.matricula === this.moto.matricula) {
            this.is_running_another_moto = false // esta runeando la misma moto
            // TODO aqui tendrá que cambiar la vista a STOP
            // TODO this.can_reserve = false
            // TODO this.can_stop = true
            // TODO ocultar todos los botones excepto el nuevo de stop
          } else { // Está runeando una moto diferente
            this.is_running_another_moto = true
            this.can_reserve = false
          }
        })
        .catch((error) => {
          // No esta runenado ninguna moto
          this.is_running_another_moto = false
          console.error(error)
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
