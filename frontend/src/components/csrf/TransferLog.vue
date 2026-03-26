<template>
  <div class="log-section">
    <div class="log-header">
      <h2 class="section-title">Transfer Log</h2>
      <button class="btn btn--ghost log-refresh" @click="fetchLog">Refresh</button>
    </div>

    <div v-if="transfers.length === 0" class="log-empty">
      No transfers yet. Use the forms above to trigger some.
    </div>

    <div v-else class="log-table-wrap">
      <table class="log-table">
        <thead>
          <tr>
            <th>Time</th>
            <th>Recipient</th>
            <th>Amount</th>
            <th>Protection</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="t in transfers"
            :key="t.id"
            :class="t.method.includes('VULNERABLE') ? 'log-row--danger' : 'log-row--safe'"
          >
            <td>{{ formatTime(t.created_at) }}</td>
            <td>{{ t.recipient }}</td>
            <td>${{ t.amount.toLocaleString() }}</td>
            <td>
              <span
                class="badge"
                :class="t.method.includes('VULNERABLE') ? 'badge--red' : 'badge--green'"
              >
                {{ t.method.includes('VULNERABLE') ? 'Unprotected' : 'CSRF Token' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/utils/api'

const transfers = ref([])

async function fetchLog() {
  try {
    transfers.value = await api.get('/api/csrf/transfers')
  } catch {
    // Not authenticated or other error
  }
}

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString()
}

onMounted(fetchLog)
</script>

<style scoped>
.log-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.log-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.log-header .section-title {
  margin-bottom: 0;
}

.log-refresh {
  padding: 6px 14px;
  font-size: 12px;
}

.log-empty {
  padding: 32px;
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
}

.log-table-wrap {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.log-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.log-table th {
  text-align: left;
  padding: 12px 16px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border-subtle);
}

.log-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-secondary);
}

.log-table tr:last-child td {
  border-bottom: none;
}

.log-row--danger td {
  background: rgba(255, 68, 68, 0.03);
}

.log-row--safe td {
  background: rgba(0, 229, 160, 0.02);
}
</style>