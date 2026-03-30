<template>
  <div class="login-page">
    <div class="login-box">
      <div class="login-brand">
        <span class="login-brand-icon">⚔</span>
        <span class="login-brand-name">SecureDemo</span>
      </div>

      <h1 class="login-title">Sign in</h1>
      <p class="login-sub">Use one of the test accounts below to explore the demos.</p>

      <div class="login-accounts">
        <button
          v-for="acct in testAccounts"
          :key="acct.username"
          class="login-account-btn"
          @click="fillAccount(acct)"
        >
          <span class="login-account-user">{{ acct.username }}</span>
          <span class="login-account-hint">click to fill</span>
        </button>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">Username</label>
          <input
            v-model="form.username"
            type="text"
            class="form-input"
            placeholder="alice or bob"
            autocomplete="username"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Password</label>
          <input
            v-model="form.password"
            type="password"
            class="form-input"
            placeholder="password123"
            autocomplete="current-password"
          />
        </div>

        <div v-if="errorMsg" class="alert alert--error">{{ errorMsg }}</div>

        <button type="submit" class="btn btn--safe login-submit" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign in →' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const testAccounts = [
  { username: 'alice', password: 'password123' },
  { username: 'bob', password: 'password123' },
]

const form = ref({ username: '', password: '' })
const loading = ref(false)
const errorMsg = ref('')

function fillAccount(acct) {
  form.value.username = acct.username
  form.value.password = acct.password
}

async function handleLogin() {
  errorMsg.value = ''
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    router.push('/')
  } catch (err) {
    errorMsg.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background:
    radial-gradient(ellipse 60% 40% at 50% 0%, rgba(0, 229, 160, 0.06) 0%, transparent 70%),
    var(--bg-base);
}

.login-box {
  width: 100%;
  max-width: 400px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.login-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-display);
  font-weight: 800;
  font-size: 15px;
  color: var(--text-muted);
}

.login-brand-icon {
  font-size: 18px;
}

.login-title {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.login-sub {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: -8px;
}

.login-accounts {
  display: flex;
  gap: 10px;
}

.login-account-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding: 10px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  transition: all var(--transition);
}

.login-account-btn:hover {
  border-color: var(--accent-green);
  background: var(--accent-green-dim);
}

.login-account-user {
  font-size: 14px;
  font-weight: 700;
}

.login-account-hint {
  font-size: 10px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.login-submit {
  width: 100%;
  padding: 12px;
  margin-top: 4px;
}
</style>