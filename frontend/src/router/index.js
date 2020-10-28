import Vue from 'vue'
import Router from 'vue-router'
import Homepage from '@/components/Homepage'
import Motos from '@/components/Motos.vue'
import HelloWorld from '@/components/HelloWorld'
import Registration from '@/components/Registration.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/Motos',
      name: 'Motos',
      component: Motos
    },
    {
      path: '/Homepage',
      name: 'Homepage',
      component: Homepage
    },
    {
      path: '/userregister',
      name: 'Registration',
      component: Registration
    }
  ]
})
