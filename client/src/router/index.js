import RoomsView from '@/views/RoomsView.vue'
import ServiceView from '@/views/ServiceView.vue'
import AccomodattionView from '@/views/AccomodattionView.vue'
import ProvisionView from '@/views/ProvisionView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "RoomsView",
      meta: { requiresAuth: true },
      component: RoomsView
    },
    {
      path: "/service",
      name: "ServiceView",
      meta: { requiresAuth: true },
      component: ServiceView
    },
    {
      path: "/accomodattion",
      name: "AccomodattionView",
      meta: { requiresAuth: true },
      component: AccomodattionView
    },
    {
      path: "/provision",
      name: "ProvisionView",
      meta: { requiresAuth: true },
      component: ProvisionView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login' }
  }
})

export default router
