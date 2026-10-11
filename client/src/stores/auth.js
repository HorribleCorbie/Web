import { defineStore } from 'pinia'
 
export const useAuthStore = defineStore('auth', {
  state: () => {
    const storedState = localStorage.getItem('authState')
    return storedState
      ? JSON.parse(storedState)
      : {
          user: null,
          isAuthenticated: false,
        }
  },
  actions: {
    async setCsrfToken() {
      await fetch(`/api/set-csrf-token`, {
        method: 'GET',
        credentials: 'include',
      })
    },
 
    async login(username, password, router = null) {
      const response = await fetch(`/api/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
          username,
          password,
        }),
        credentials: 'include',
      })
      const data = await response.json()
      if (response.ok && data.success) {
        await this.fetchUser()

        if (this.isAuthenticated && router) {
          await router.push('/')
        }
      } else {
        this.user = null
        this.isAuthenticated = false
        this.saveState()
      }
    },
 
    async logout(router = null) {
      try {
        const response = await fetch(`/api/logout/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
        })
        if (response.ok) {
          this.user = null
          this.isAuthenticated = false
          this.saveState()
          if (router) {
            await router.push({
              name: 'login',
            })
          }
        }
      } catch (error) {
        console.error('Logout failed', error)
        throw error
      }
    },
 
    async fetchUser() {
      try {
        const response = await fetch(`/api/user/`, {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
        })
        if (response.ok) {
          const data = await response.json()
          this.user = data
          this.isAuthenticated = true
        } else {
          this.user = null
          this.isAuthenticated = false
        }
      } catch (error) {
        console.error('Failed to fetch user', error)
        this.user = null
        this.isAuthenticated = false
      }
      this.saveState()
    },
 
    saveState() {
      localStorage.setItem(
        'authState',
        JSON.stringify({
          user: this.user,
          isAuthenticated: this.isAuthenticated,
        }),
      )
    },
  },
})
 
export function getCSRFToken() {
  const name = 'csrftoken'
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  if (cookieValue === null) {
    throw 'Missing CSRF cookie.'
  }
  return cookieValue
}