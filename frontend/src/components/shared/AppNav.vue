<template>
  <nav class="nav">
    <div class="nav__inner container">
      <RouterLink to="/" class="nav__logo">
        <span class="nav__logo-icon">⚔</span>
        <span>SecureDemo</span>
      </RouterLink>

      <div class="nav__links">
        <RouterLink to="/csrf" class="nav__link" active-class="nav__link--active">
          CSRF
        </RouterLink>
        <RouterLink to="/xss" class="nav__link" active-class="nav__link--active">
          XSS
        </RouterLink>
      </div>

      <div class="nav__user">
        <div class="nav__user-info">
          <span class="nav__username">{{ auth.user?.username }}</span>
          <span class="nav__balance">${{ auth.user?.balance?.toLocaleString() }}</span>
        </div>
        <button class="btn btn--ghost nav__logout" @click="handleLogout">
          Logout
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

async function handleLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(10, 10, 15, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-subtle);
}

.nav__inner {
  display: flex;
  align-items: center;
  gap: 32px;
  height: 60px;
}

.nav__logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-display);
  font-weight: 800;
  font-size: 16px;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.nav__logo-icon {
  font-size: 18px;
}

.nav__links {
  display: flex;
  gap: 4px;
  flex: 1;
}

.nav__link {
  padding: 6px 14px;
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
  transition: all var(--transition);
}

.nav__link:hover {
  color: var(--text-primary);
  background: var(--bg-elevated);
}

.nav__link--active {
  color: var(--text-primary);
  background: var(--bg-elevated);
}

.nav__user {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav__user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 1px;
}

.nav__username {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.nav__balance {
  font-size: 11px;
  color: var(--accent-green);
}

.nav__logout {
  padding: 6px 14px;
  font-size: 12px;
}
</style>