import {createApp} from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import AdminDashboard from '../views/AdminDashboard.vue'
import SponsorDashboard from '../views/SponsorDashboard.vue'
import InfluencerDashboard from '../views/InfluencerDashboard.vue'
import SponsorLogin from '../components/SponsorLogin.vue'
import InfluencerLogin from '../components/InfluencerLogin.vue'
import SponsorRegister from '../components/SponsorRegister.vue'
import InfluencerRegister from '../components/InfluencerRegister.vue'


const routes = [
  { path: '/', redirect: '/sponsor/login' },
  { path: '/sponsor/login', component: SponsorLogin },
  { path: '/influencer/login', component: InfluencerLogin },
  { path: '/sponsor/register', component: SponsorRegister },
  { path: '/influencer/register', component: InfluencerRegister },
  { path: '/admin', component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/sponsor', component: SponsorDashboard, meta: { requiresAuth: true, role: 'sponsor' } },
  { path: '/influencer', component: InfluencerDashboard, meta: { requiresAuth: true, role: 'influencer' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('user')
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!loggedIn) {
      next('/login')
    } else {
      let userRole;
      if(JSON.parse(loggedIn).sp_id){
        userRole = 'sponsor'
      } else if(JSON.parse(loggedIn).inf_id){
        userRole = 'influencer'
      } else {
        userRole = 'admin'
      }
      if (to.meta.role !== userRole) {
        next('/login')
      } else {
        next()
      }
    }
  } else {
    next()
  }
})

export default router
