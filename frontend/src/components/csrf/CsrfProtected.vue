<template>
  <div class="card card--safe">
    <div class="section-header">
      <span class="badge badge--green">Protected</span>
      <h2 class="section-title">CSRF Token Validated</h2>
    </div>

    <p class="panel-desc">
      This endpoint requires a CSRF token that matches the one stored in your server-side session.
      An attacker on a different origin cannot read your session token, so forged requests are rejected.
    </p>

    <div class="code-block">
<span class="cm"># ✅ Endpoint validates CSRF token before processing</span>
<span class="kw">@router</span>.post(<span class="str">"/transfer/secure"</span>)
<span class="kw">def</span> <span class="fn">transfer_secure</span>(payload, request):
    session_token = request.session.<span class="fn">get</span>(<span class="str">"csrf_token"</span>)
    <span class="kw">if</span> session_token != payload.csrf_token:
        <span class="kw">raise</span> <span class="fn">HTTPException</span>(<span class="var">403</span>, <span class="str">"CSRF token invalid"</span>)
    log_transfer(username, payload.recipient, payload.amount)
</div>

    <div class="divider" />

    <div class="token-display">
      <span class="token-label">Your CSRF Token</span>
      <span class="token-value">{{ auth.csrfToken ? auth.csrfToken.slice(0, 20) + '...' : 'Not set' }}</span>
    </div>

    <form class="panel-form" @submit.prevent="handleTransfer">
      <div class="form-group">
        <label class="form-label">Recipient</label>
        <input v-model="form.recipient" type="text" class="form-input" placeholder="bob" />
      </div>
      <div class="form-group">
        <label class="form-label">Amount ($)</label>
        <input v-model="form.amount" type="number" class="form-input" placeholder="100" min="1" />
      </div>

      <div v-if="result" class="alert" :class="result.type === 'error' ? 'alert--error' : 'alert--success'">
        {{ result.message }}
      </div>

      <button type="submit" class="btn btn--safe" :disabled="loading">
        {{ loading ? 'Sending...' : 'Transfer (With CSRF Token)' }}
      </button>
    </form>

    <div class="attacker-sim">
      <div class="attacker-sim__header">
        <span class="badge badge--green">Attack Attempt</span>
      </div>
      <p class="attacker-sim__desc">
        Simulate an attacker trying to forge a request to this protected endpoint.
        Without the real CSRF token, the server will reject it with 403.
      </p>
      <button class="btn btn--ghost" @click="simulateAttack" :disabled="attackLoading">
        {{ attackLoading ? 'Attempting...' : '⛔ Try Forged Request (Should Fail)' }}
      </button>
      <div v-if="attackResult" class="alert alert--success" style="margin-top: 12px;">
        {{ attackResult }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '@/utils/api'
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits(['transferred'])
const auth = useAuthStore()

const form = ref({ recipient: 'bob', amount: 100 })
const loading = ref(false)
const result = ref(null)

const attackLoading = ref(false)
const attackResult = ref('')

async function handleTransfer() {
  loading.value = true
  result.value = null
  try {
    const data = await api.post('/api/csrf/transfer/secure', {
      recipient: form.value.recipient,
      amount: Number(form.value.amount),
      csrf_token: auth.csrfToken,
    })
    result.value = {
      type: 'success',
      message: `Transfer succeeded: ${data.message}`,
    }
    emit('transferred')
  } catch (err) {
    result.value = { type: 'error', message: err.message }
  } finally {
    loading.value = false
  }
}

async function simulateAttack() {
  attackLoading.value = true
  attackResult.value = ''
  try {
    await api.post('/api/csrf/transfer/secure', {
      recipient: 'attacker',
      amount: 9999,
      csrf_token: 'fake-attacker-token-abc123',
    })
    attackResult.value = 'Unexpected: attack succeeded. Check your CSRF configuration.'
  } catch (err) {
    attackResult.value = `Forged request blocked: ${err.message}. CSRF protection worked.`
    emit('transferred')
  } finally {
    attackLoading.value = false
  }
}
</script>

<style scoped>
.panel-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 16px;
}

.token-display {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  background: var(--bg-base);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  margin-bottom: 16px;
}

.token-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  font-weight: 700;
  white-space: nowrap;
}

.token-value {
  font-size: 12px;
  color: var(--accent-green);
  word-break: break-all;
}

.panel-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.attacker-sim {
  margin-top: 20px;
  padding: 16px;
  background: rgba(0, 229, 160, 0.04);
  border: 1px dashed rgba(0, 229, 160, 0.25);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.attacker-sim__header {
  display: flex;
  align-items: center;
}

.attacker-sim__desc {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.6;
}
</style>