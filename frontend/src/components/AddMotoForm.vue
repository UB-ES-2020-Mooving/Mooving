<template>
  <div id="wholePage">
    <b-navbar toggleable type="dark" variant="dark">
        <b-navbar-brand href="#">
          <img src="./Images/moovingLogoBlanco.png" alt= "Logo" style= "width:100px;">
        </b-navbar-brand>
    </b-navbar>
    <div class="jumbotron">
      <div class="container">
        <div class="row">
          <div class="col-sm-8 offset-sm-2">
            <div>
              <h2>Motorbike Form</h2>
              <form @submit.prevent="handleSubmit">
                <div class="form-group">
                  <label for="licensePlate">License Plate</label>
                  <input type="text" v-model="moto.licensePlate" id="licensePlate" name="licensePlate" class="form-control" :class="{ 'is-invalid': submitted && $v.moto.licensePlate.$error }" />
                  <div v-if="submitted && $v.moto.licensePlate.$error" class="invalid-feedback">
                    <span v-if="!$v.moto.licensePlate.required">Please, complete the form</span>
                    <span v-if="!$v.moto.licensePlate.minLength">License Plate must be at least 8 characters</span>
                  </div>
                </div>
                <div class="form-group">
                  <label for="type">Type</label>
                  <select v-model="moto.type" id="type" name="type" class="form-control" :class="{ 'is-invalid': submitted && $v.moto.type.$error }" >
                    <option disabled value="">Select type</option>
                    <option>Basic</option>
                    <option>Premium</option>
                  </select>
                  <div v-if="submitted && $v.moto.type.$error" class="invalid-feedback">
                    <span v-if="!$v.moto.type.required">Please, complete the form</span>
                  </div>
                </div>
                <div class="form-group">
                  <button class="btn"
                      id="cancelButton"
                      type="button"
                      @click="cancel()"
                      style="margin-top: 20px;margin-left: 10px;border-radius: 12px;
                      background-color: #ff6961;color: #ffffff; width: 140px">
                    Cancel
                  </button>
                  <button class="btn btn-primary" style="margin-top: 20px;margin-left: 5px;border-radius: 12px; background-color: #343a40;color: #42b983; width: 140px">Confirm</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { required, email, minLength, maxLength, sameAs } from 'vuelidate/lib/validators'
import axios from 'axios'

export default {
  name: 'MotoForm',
  data () {
    return {
      email: '',
      moto: {
        licensePlate: '',
        type: ''
      },
      submitted: false
    }
  },
  validations: {
    moto: {
      licensePlate: { required, minLength: minLength(8) },
      type: { required }
    }
  },
  created () {
    this.email = this.$route.query.email
  },
  methods: {
    handleSubmit (e) {
      this.submitted = true

      // stop here if form is invalid
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }
    },
    cancel(){
      this.$router.push({ path: '/motospagemechanic', query: { email: this.email } })
    }
  }
}
</script>

<style scoped>
#wholePage
  {
  position:fixed;
  padding:0;
  margin:0;
  top:0;
  left:0;
  width: 100%;
  height: 100%;
  background-color: #e9ecef;
  }
</style>
