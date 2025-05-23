import {createApp} from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import AdminDashboard from '../views/AdminDashboard'
import SponsorDashboard from '../views/Sponsors/SponsorDashboard'
import InfluencerDashboard from '../views/Influencers/InfluencerDashboard'
import SponsorLogin from '../components/Sponsors/SponsorLogin'
import InfluencerLogin from '../components/Influencers/InfluencerLogin'
import AdminLogin from '@/components/AdminLogin'
import SponsorRegister from '../components/Sponsors/SponsorRegister'
import InfluencerRegister from '../components/Influencers/InfluencerRegister'
import HomeView from '@/views/HomeView'
import Campaigns from '@/views/Campaigns'
import Connect from '@/views/Connect'

const routes = [
  { path: '/', component: HomeView },
  { path: '/sponsor/login', component: SponsorLogin },
  { path: '/influencer/login', component: InfluencerLogin },
  { path: '/sponsor/register', component: SponsorRegister },
  { path: '/influencer/register', component: InfluencerRegister },
  { path: '/admin/login', component: AdminLogin },
  { path: '/admin', component: AdminDashboard, meta: { requiresAuth: true, role: ['admin'] } },
  { path: '/sponsor', component: SponsorDashboard, meta: { requiresAuth: true, role: ['sponsor'] } },
  { path: '/influencer', component: InfluencerDashboard, meta: { requiresAuth: true, role: ['influencer'] } },
  { path: '/campaigns', component: Campaigns, meta: { requiresAuth: true , role: ['influencer', 'sponsor']} },
  { path: '/connect', component: Connect, meta: { requiresAuth: true , role: ['influencer', 'sponsor']} },
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
      next('/'+to.meta.role[0]+'/login')
    } else {
      let userRole;
      if(JSON.parse(loggedIn).sp_id){
        userRole = 'sponsor'
      } else if(JSON.parse(loggedIn).inf_id){
        userRole = 'influencer'
      } else {
        userRole = 'admin'
      }
      localStorage.setItem('userRole', userRole);
      if (!to.meta.role.includes(userRole)) {
        next('/'+to.meta.role[0]+'/login')
      } else {
        next()
      }
    }
  } else {
    next()
  }
})

export default router
