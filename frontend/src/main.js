// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import '@/../bootstrap/css/bootstrap.css'
import Vue from 'vue'
import Vuelidate from 'vuelidate'
import App from './App.vue'
import router from './router'

Vue.use(BootstrapVue)
Vue.use(Vuelidate)
Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

new Vue({
  router,
  render: (h) => h(App)
}).$mount('#app')
