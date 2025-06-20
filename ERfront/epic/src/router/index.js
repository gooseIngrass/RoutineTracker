// src/router.js
import { createRouter, createWebHistory } from 'vue-router'
import TasksView from '../views/TaskView.vue'
import ProfileView from '../views/ProfileView.vue'
import WelcomeView from '../views/WelcomeView.vue'
import DungeonView from '@/views/DungeonView.vue'
import GuildView from '@/views/GuildView.vue'

const routes = [
  {
    path: '/',
    name: 'Tasks',
    component: TasksView
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView
  }, 
  {
    path: '/welcome',
    name: 'Welcome',
    component: WelcomeView
  },
  {
    path: '/dungeon',
    name: 'Dungeon',
    component: DungeonView
  },
  {
    path: '/guild',
    name: 'Guild',
    component: GuildView
  }
]

const router = createRouter({
  history:createWebHistory(import.meta.env.BASE_URL),
  routes
})



export default router