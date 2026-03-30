<template>
  <div class="card card--safe">
    <div class="section-header">
      <span class="badge badge--green">Protected</span>
      <h2 class="section-title">Input Sanitized (bleach)</h2>
    </div>

    <p class="panel-desc">
      Comments are sanitized with Python's <code>bleach</code> library before being stored.
      Only a small allowlist of safe HTML tags is permitted. Script tags, event handlers,
      and all other dangerous constructs are stripped. The frontend also uses <code>v-text</code>
      instead of <code>v-html</code> as an additional layer.
    </p>

    <div class="code-block">
<span class="cm"># ✅ Backend sanitizes before storage</span>
<span class="kw">import</span> bleach

ALLOWED_TAGS = [<span class="str">"b"</span>, <span class="str">"i"</span>, <span class="str">"u"</span>, <span class="str">"em"</span>, <span class="str">"strong"</span>]

<span class="kw">def</span> <span class="fn">post_comment_secure</span>(payload, request):
    sanitized = bleach.<span class="fn">clean</span>(
        payload.content,
        tags=ALLOWED_TAGS,
        strip=<span class="var">True</span>,
    )
    add_comment_safe(author=username, content=sanitized)

<span class="cm">// ✅ Frontend uses v-text — no HTML interpretation</span>
&lt;p <span class="var">v-text</span>=<span class="str">"comment.content"</span>&gt;&lt;/p&gt;
</div>

    <div class="divider" />

    <form class="panel-form" @submit.prevent="submitComment">
      <div class="form-group">
        <label class="form-label">Comment (try the same XSS payloads)</label>
        <textarea v-model="commentText" class="form-input form-textarea" rows="3" />
      </div>

      <div v-if="errorMsg" class="alert alert--error">{{ errorMsg }}</div>

      <button type="submit" class="btn btn--safe" :disabled="loading">
        {{ loading ? 'Posting...' : 'Post Comment (Sanitized)' }}
      </button>
    </form>

    <div v-if="comments.length > 0" class="comments">
      <p class="comments-label">Rendered Comments <span class="badge badge--green">v-text</span></p>
      <div class="comment-list">
        <div v-for="c in comments" :key="c.id" class="comment">
          <div class="comment__meta">
            <span class="comment__author">{{ c.author }}</span>
            <span class="comment__time">{{ formatTime(c.created_at) }}</span>
          </div>

          <!-- Safe: v-text treats the value as a plain string, no HTML execution -->
          <p class="comment__body" v-text="c.content" />

          <div v-if="c.raw_content !== c.content" class="comment__diff">
            <span class="diff-label">Raw input:</span>
            <code class="diff-raw">{{ c.raw_content }}</code>
            <span class="diff-label">After sanitization:</span>
            <code class="diff-clean">{{ c.content }}</code>
          </div>
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

async function submitComment() {
  errorMsg.value = ''
  loading.value = true
  try {
    await api.post('/api/xss/comment/secure', { content: commentText.value })
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
    comments.value = await api.get('/api/xss/comments/secure')
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
  border: 1px solid rgba(0, 229, 160, 0.12);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.comment__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.comment__diff {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 10px;
  background: var(--bg-base);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  margin-top: 4px;
}

.diff-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--text-muted);
}

.diff-raw {
  font-size: 11px;
  color: var(--accent-red);
  word-break: break-all;
  font-family: var(--font-mono);
}

.diff-clean {
  font-size: 11px;
  color: var(--accent-green);
  word-break: break-all;
  font-family: var(--font-mono);
}
</style>