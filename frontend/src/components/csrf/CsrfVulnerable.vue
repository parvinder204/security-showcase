<template>
  <div class="card card--danger">
    <div class="section-header">
      <span class="badge badge--red">Vulnerable</span>
      <h2 class="section-title">No CSRF Protection</h2>
    </div>

    <p class="panel-desc">
      This endpoint accepts any POST request as long as a valid session cookie is present.
      No CSRF token is required — a forged request from another site will succeed.
    </p>

    <div class="code-block">
<span class="cm"># ❌ Endpoint only checks session — no token validation</span>
<span class="kw">@router</span>.post(<span class="str">"/transfer/vulnerable"</span>)
<span class="kw">def</span> <span class="fn">transfer_vulnerable</span>(payload, request):
    username = request.session.<span class="fn">get</span>(<span class="str">"username"</span>)
    <span class="cm"># No CSRF check — attacker can forge this!</span>
    log_transfer(username, payload.recipient, payload.amount)
</div>

    <div class="divider" />

    <form class="panel-form" @submit.prevent="handleTransfer">
      <div class="form-group">
        <label class="form-label">Recipient</label>
        <input v-model="form.recipient" type="text" class="form-input" placeholder="bob" />
      </div>
      <div class="form-group">
        <label class="form-label">Amount ($)</label>
        <input v-model="form.amount" type="number" class="form-input" placeholder="100" min="1" />
      </div>

      <div v-if="result" class="alert" :class="result.type === 'error' ? 'alert--error' : 'alert--warning'">
        {{ result.message }}
      </div>

      <button type="submit" class="btn btn--danger" :disabled="loading">
        {{ loading ? 'Sending...' : 'Transfer (No CSRF Token)' }}
      </button>
    </form>

    <div class="attacker-sim">
      <div class="attacker-sim__header">
        <span class="badge badge--red">Attacker Simulation</span>
      </div>
      <p class="attacker-sim__desc">
        Click to simulate what a malicious page would do. It fires a request
        to the vulnerable endpoint without any CSRF token — and it will succeed.
      </p>
      <button class="btn btn--ghost" @click="simulateAttack" :disabled="attackLoading">
        {{ attackLoading ? 'Forging...' : '⚡ Simulate Forged Request' }}
      </button>
      <div v-if="attackResult" class="alert alert--error" style="margin-top: 12px;">
        {{ attackResult }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '@/utils/api'

const emit = defineEmits(['transferred'])

const form = ref({ recipient: 'bob', amount: 100 })
const loading = ref(false)
const result = ref(null)

const attackLoading = ref(false)
const attackResult = ref('')

async function handleTransfer() {
  loading.value = true
  result.value = null
  try {
    const data = await api.post('/api/csrf/transfer/vulnerable', {
      recipient: form.value.recipient,
      amount: Number(form.value.amount),
    })
    result.value = {
      type: 'warning',
      message: `⚠ Transfer succeeded: ${data.message} (${data.warning})`,
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
    // Simulates a request that an attacker's page would fire — no token included
    const data = await api.post('/api/csrf/transfer/vulnerable', {
      recipient: 'attacker',
      amount: 9999,
    })
    attackResult.value = `Attack succeeded! ${data.message} The server processed the forged transfer.`
    emit('transferred')
  } catch (err) {
    attackResult.value = `Attack blocked: ${err.message}`
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

.panel-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.attacker-sim {
  margin-top: 20px;
  padding: 16px;
  background: rgba(255, 68, 68, 0.05);
  border: 1px dashed rgba(255, 68, 68, 0.3);
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