<template>
  <div class="page container">
    <div class="page-header">
      <div class="page-header__meta">
        <span class="badge badge--amber">Attack Demo</span>
      </div>
      <h1 class="page-title">Cross-Site Scripting</h1>
      <p class="page-desc">
        XSS allows attackers to inject malicious JavaScript into pages viewed by other users.
        Unlike CSRF, which abuses server trust, XSS abuses user trust in your application —
        injected scripts run in your users' browsers with full access to their session data.
      </p>
    </div>

    <div class="xss-types">
      <h2 class="section-title">Types of XSS</h2>
      <div class="types-grid">
        <div class="type-card type-card--stored">
          <div class="type-card__badge badge badge--red">Stored (Persistent)</div>
          <h3 class="type-card__title">Stored XSS</h3>
          <p class="type-card__desc">
            Malicious script is saved in the database and served to every user who visits the page.
            This is what we demo below — the most dangerous type.
          </p>
        </div>
        <div class="type-card">
          <div class="type-card__badge badge badge--amber">Reflected</div>
          <h3 class="type-card__title">Reflected XSS</h3>
          <p class="type-card__desc">
            Script comes from a URL parameter. Victim must click a crafted link.
            Dangerous but only affects users who click the specific URL.
          </p>
        </div>
        <div class="type-card">
          <div class="type-card__badge badge badge--amber">DOM-Based</div>
          <h3 class="type-card__title">DOM XSS</h3>
          <p class="type-card__desc">
            Script is injected through client-side JavaScript that reads from
            URL fragments or storage and writes to the DOM unsafely.
          </p>
        </div>
      </div>
    </div>

    <div class="demo-grid">
      <XssVulnerable />
      <XssProtected />
    </div>

    <div class="explainer">
      <h2 class="section-title">Why the Fix Works</h2>
      <div class="explainer__grid">
        <div class="explainer__item">
          <h3 class="explainer__label">Input Sanitization (bleach)</h3>
          <p class="explainer__text">
            The <code>bleach.clean()</code> function parses the HTML and strips any tags or
            attributes not in the allowlist. Even if an attacker submits
            <code>&lt;script&gt;alert(1)&lt;/script&gt;</code>, it is reduced to plain text before storage.
            The attacker's code never reaches the database.
          </p>
        </div>
        <div class="explainer__item">
          <h3 class="explainer__label">Avoid innerHTML</h3>
          <p class="explainer__text">
            When rendering user content on the frontend, using <code>v-html</code> in Vue or
            <code>innerHTML</code> in plain JS executes embedded scripts.
            Use <code>v-text</code> or <code>textContent</code> instead —
            they treat the value as a plain string, never as HTML.
          </p>
        </div>
        <div class="explainer__item">
          <h3 class="explainer__label">Content Security Policy</h3>
          <p class="explainer__text">
            A CSP header like <code>script-src 'self'</code> tells the browser to refuse
            executing any script that did not originate from your own domain.
            Even if XSS code is injected, the browser will refuse to run it.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import XssVulnerable from '@/components/xss/XssVulnerable.vue'
import XssProtected from '@/components/xss/XssProtected.vue'
</script>

<style scoped>
.page {
  padding-top: 60px;
  padding-bottom: 80px;
  display: flex;
  flex-direction: column;
  gap: 56px;
}

.page-header__meta {
  margin-bottom: 16px;
}

.page-title {
  font-size: clamp(32px, 5vw, 52px);
  font-weight: 800;
  letter-spacing: -0.02em;
  margin-bottom: 16px;
}

.page-desc {
  max-width: 660px;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.75;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 20px;
}

.types-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.type-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.type-card--stored {
  border-color: rgba(255, 68, 68, 0.25);
}

.type-card__badge {
  align-self: flex-start;
}

.type-card__title {
  font-size: 15px;
  font-weight: 700;
  font-family: var(--font-display);
}

.type-card__desc {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.65;
}

.demo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 20px;
}

.explainer__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}

.explainer__item {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.explainer__label {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: var(--font-display);
}

.explainer__text {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.explainer__text code {
  font-family: var(--font-mono);
  background: var(--bg-elevated);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  color: var(--accent-amber);
}
</style>