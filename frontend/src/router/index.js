import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Registration from '@/components/Registration.vue'
import Login from '@/components/Login.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
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
    }
  ]
})
