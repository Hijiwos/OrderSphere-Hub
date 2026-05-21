import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Menu from '../views/Menu.vue'
import Checkout from '../views/Checkout.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Admin from '../views/Admin.vue'
import UserProfile from '../views/UserProfile.vue'
import ChangePassword from '../views/ChangePassword.vue'
import Inventory from '../views/inventory.vue'
import In from '../views/in.vue'
import Out from '../views/out.vue'
import Alerts from '../views/alerts.vue'
import Notifications from '../views/notifications.vue'

const routes = [
  { path: '/', redirect: '/menu' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/menu', component: Menu },
  { path: '/checkout', component: Checkout },
  { path: '/admin', component: Admin },
  { path: '/profile', component: UserProfile },
  { path: '/change-password', component: ChangePassword },
  { path: '/inventory', component: Inventory },
  { path: '/in', component: In },
  { path: '/out', component: Out },
  { path: '/alerts', component: Alerts },
  { path: '/notifications', component: Notifications },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router