import Vue from 'vue'
import Router from 'vue-router'
import Motos from '@/components/Motos.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/Motos',
      name: 'Motos',
      component: Motos
    }
  ]
})
