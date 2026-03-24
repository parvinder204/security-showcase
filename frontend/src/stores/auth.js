import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/utils/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const csrfToken = ref(null)

  const isLoggedIn = computed(() => user.value !== null)

  async function login(username, password) {
    const data = await api.post('/api/auth/login', { username, password })
    user.value = {
      username: data.username,
      email: data.email,
      balance: data.balance,
    }
    csrfToken.value = data.csrf_token
  }

  async function logout() {
    await api.post('/api/auth/logout', {})
    user.value = null
    csrfToken.value = null
  }

  async function fetchMe() {
    try {
      const data = await api.get('/api/auth/me')
      user.value = {
        username: data.username,
        email: data.email,
        balance: data.balance,
      }
      csrfToken.value = data.csrf_token
    } catch {
      user.value = null
      csrfToken.value = null
    }
  }

  return { user, csrfToken, isLoggedIn, login, logout, fetchMe }
})