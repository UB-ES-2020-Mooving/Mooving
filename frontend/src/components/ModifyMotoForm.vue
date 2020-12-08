<template>
  <div class="jumbotron">
    <div class="container">
      <div class="row">
        <div class="col-sm-8 offset-sm-2">
          <div>
            <h2>Modify Motorbike Form</h2>
            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                <label for="licensePlate">License Plate</label>
                <input type="text" v-model="moto.licensePlate" id="licensePlate" name="licensePlate" class="form-control" :class="{ 'is-invalid': submitted && $v.moto.licensePlate.$error }" />
                <div v-if="submitted && $v.moto.licensePlate.$error" class="invalid-feedback">
                  <span v-if="!$v.moto.licensePlate.required">License Plate is required</span>
                  <span v-if="!$v.moto.licensePlate.minLength">License Plate must be at least 8 characters</span>
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
                <button class="btn btn-primary" style="margin-top: 20px;margin-left: 5px;border-radius: 12px; background-color: #343a40;color: #42b983; width: 140px">Save</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { required, minLength } from 'vuelidate/lib/validators'
import axios from 'axios'
export default {
  name: 'ModifyMotoForm',
  data () {
    return {
      email: '',
      id: 0,
      moto: {
        licensePlate: ''
      },
      submitted: false
    }
  },
  validations: {
    moto: {
      licensePlate: {
        required,
        minLength: minLength(8)
      }
    }
  },
  created () {
    this.email = this.$route.query.email
    this.id = this.$route.query.id
  },
  methods: {
    cancel () {
      alert('cancel')
      this.$router.push({ path: '/mechanicMoto', query: { id: this.id, email: this.email } })
    },
    handleSubmit (e) {
      this.submitted = true
      alert('ha entrado')
      // stop here if form is invalid
      this.$v.$touch()
      if (this.$v.$invalid) {
        alert('ERROR')
      }
    }
  }
}
</script>

<style scoped>
</style>
