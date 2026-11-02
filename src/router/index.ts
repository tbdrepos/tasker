import { createRouter, createWebHistory } from 'vue-router'
import App from '@/App.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [{ path: '/', component: App }],
})

router.beforeEach(async (to, from) => {
  const authStore = useAuthStore()

  // Protect routes requiring auth
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Redirect to login BEFORE the target component mounts
    return { name: 'Login' }
  }
})

export default router
