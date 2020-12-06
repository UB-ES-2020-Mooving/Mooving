import Vue from 'vue'
import Router from 'vue-router'
import Homepage from '@/components/Homepage'
import MotosMechanic from '@/components/MotosMechanic.vue'
import Registration from '@/components/Registration.vue'
import Login from '@/components/Login.vue'
import Profile from '@/components/Profile.vue'
import MotosClient from '@/components/MotosClient'
import clientMoto from '../components/clientMoto'
import mechanicMoto from '../components/MechanicMoto'
import ConfirmDeleteAccountDialog from '@/components/ConfirmDeleteAccountDialog.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/motospagemechanic',
      name: 'MotosMechanic',
      component: MotosMechanic
    },
    {
      path: '/motospageclient',
      name: 'MotosClient',
      component: MotosClient
    },
    {
      path: '/',
      name: 'Homepage',
      component: Homepage
    },
    {
      path: '/userregister',
      name: 'Registration',
      component: Registration
    },
    {
      path: '/userlogin',
      name: 'Login',
      component: Login
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile
    },
    {
      path: '/clientMoto',
      name: 'clientMoto',
      component: clientMoto
    },
    {
      path: '/mechanicMoto',
      name: 'mechanicMoto',
      component: mechanicMoto
    },
    {
      path: '/confirmDeleteAccount',
      name: 'confirmDeleteAccount',
      component: ConfirmDeleteAccountDialog
    }
  ]
})
