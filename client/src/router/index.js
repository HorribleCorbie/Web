import RoomsView from '@/views/RoomsView.vue'
import ServiceView from '@/views/ServiceView.vue'
import AccomodattionView from '@/views/AccomodattionView.vue'
import ProvisionView from '@/views/ProvisionView.vue'
import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "RoomsView",
      component: RoomsView
    },
    {
      path: "/service",
      name: "ServiceView",
      component: ServiceView
    },
    {
      path: "/accomodattion",
      name: "AccomodattionView",
      component: AccomodattionView
    },
    {
      path: "/provision",
      name: "ProvisionView",
      component: ProvisionView
    }
  ],
})

export default router
