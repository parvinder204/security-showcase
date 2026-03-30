<template>
  <div class="card card--danger">
    <div class="section-header">
      <span class="badge badge--red">Vulnerable</span>
      <h2 class="section-title">Raw HTML Rendered</h2>
    </div>

    <p class="panel-desc">
      Comments are stored and returned as-is with no sanitization. The frontend renders
      them using <code>v-html</code> which interprets the content as real HTML.
      Any script tag you submit will execute in the browser.
    </p>

    <div class="code-block">
<span class="cm"># ❌ Backend stores content without sanitization</span>
<span class="kw">def</span> <span class="fn">post_comment_vulnerable</span>(payload, request):
    <span class="cm"># Raw user input saved directly to database</span>
    add_comment_unsafe(author=username, content=payload.content)

<span class="cm">// ❌ Frontend renders with v-html — executes scripts</span>
&lt;p <span class="var">v-html</span>=<span class="str">"comment.content"</span>&gt;&lt;/p&gt;
</div>

    <div class="xss-payloads">
      <p class="payloads-label">Try these XSS payloads:</p>
      <div class="payload-list">
        <button
          v-for="p in payloads"
          :key="p.label"
          class="payload-btn"
          @click="fillPayload(p.value)"
        >
          {{ p.label }}
        </button>
      </div>
    </div>

    <div class="divider" />

    <form class="panel-form" @submit.prevent="submitComment">
      <div class="form-group">
        <label class="form-label">Comment (try injecting a script)</label>
        <textarea v-model="commentText" class="form-input form-textarea" rows="3" />
      </div>

      <div v-if="errorMsg" class="alert alert--error">{{ errorMsg }}</div>

      <button type="submit" class="btn btn--danger" :disabled="loading">
        {{ loading ? 'Posting...' : 'Post Comment (No Sanitization)' }}
      </button>
    </form>

    <div v-if="comments.length > 0" class="comments">
      <p class="comments-label">Rendered Comments <span class="badge badge--red">v-html</span></p>
      <div class="comment-list">
        <div v-for="c in comments" :key="c.id" class="comment">
          <div class="comment__meta">
            <span class="comment__author">{{ c.author }}</span>
            <span class="comment__time">{{ formatTime(c.created_at) }}</span>
          </div>
          <!-- This is the vulnerability: v-html renders user content as real HTML -->
          <div class="comment__body" v-html="c.content" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/utils/api'

const commentText = ref('')
const comments = ref([])
const loading = ref(false)
const errorMsg = ref('')

const payloads = [
  { label: 'Alert popup', value: '<script>alert("XSS! Your cookie: " + document.cookie)<\/script>' },
  { label: 'Image onerror', value: '<img src="x" onerror="alert(\'XSS via onerror\')">' },
  { label: 'Bold tag (harmless)', value: '<b>This is bold</b> and <i>italic</i>' },
]

function fillPayload(value) {
  commentText.value = value
}

async function submitComment() {
  errorMsg.value = ''
  loading.value = true
  try {
    await api.post('/api/xss/comment/vulnerable', { content: commentText.value })
    commentText.value = ''
    await fetchComments()
  } catch (err) {
    errorMsg.value = err.message
  } finally {
    loading.value = false
  }
}

async function fetchComments() {
  try {
    comments.value = await api.get('/api/xss/comments/vulnerable')
  } catch {
    // silently ignore
  }
}

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString()
}

onMounted(fetchComments)
</script>

<style scoped>
.panel-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 16px;
}

.panel-desc code {
  font-family: var(--font-mono);
  background: var(--bg-elevated);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--accent-amber);
}

.xss-payloads {
  margin: 16px 0;
}

.payloads-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.payload-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.payload-btn {
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  color: var(--accent-red);
  font-size: 11px;
  padding: 5px 10px;
  transition: all var(--transition);
  font-family: var(--font-mono);
}

.payload-btn:hover {
  border-color: var(--accent-red);
  background: var(--accent-red-dim);
}

.panel-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.comments {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comments-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--text-muted);
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.comment {
  background: var(--bg-elevated);
  border: 1px solid rgba(255, 68, 68, 0.15);
  border-radius: var(--radius-md);
  padding: 12px 14px;
}

.comment__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.comment__author {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-primary);
}

.comment__time {
  font-size: 11px;
  color: var(--text-muted);
}

.comment__body {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  word-break: break-word;
}
</style>