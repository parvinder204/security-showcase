<template>
  <div class="page container">
    <div class="page-header">
      <div class="page-header__meta">
        <span class="badge badge--red">Attack Demo</span>
      </div>
      <h1 class="page-title">Cross-Site Request Forgery</h1>
      <p class="page-desc">
        CSRF abuses the fact that browsers automatically attach cookies to every request,
        regardless of which site triggered it. An attacker can forge a request to your
        authenticated API from a completely different domain — and the server cannot tell the difference.
      </p>
    </div>

    <div class="how-it-works">
      <h2 class="section-title">How It Works</h2>
      <div class="flow">
        <div class="flow__step">
          <div class="flow__num">1</div>
          <div class="flow__text">User logs in and receives a session cookie</div>
        </div>
        <div class="flow__arrow">→</div>
        <div class="flow__step">
          <div class="flow__num">2</div>
          <div class="flow__text">User visits attacker's site while still logged in</div>
        </div>
        <div class="flow__arrow">→</div>
        <div class="flow__step">
          <div class="flow__num">3</div>
          <div class="flow__text">Attacker's page silently fires a request to your bank</div>
        </div>
        <div class="flow__arrow">→</div>
        <div class="flow__step flow__step--danger">
          <div class="flow__num">4</div>
          <div class="flow__text">Browser auto-attaches cookie → server accepts it as legitimate</div>
        </div>
      </div>
    </div>

    <div class="demo-grid">
      <CsrfVulnerable />
      <CsrfProtected />
    </div>

    <TransferLog />

    <div class="explainer">
      <h2 class="section-title">Why the Fix Works</h2>
      <div class="explainer__grid">
        <div class="explainer__item">
          <h3 class="explainer__label">CSRF Token</h3>
          <p class="explainer__text">
            A secret random value tied to the user's session. The server sets it on login.
            The legitimate frontend reads it and sends it back in every mutating request.
            An attacker on another origin cannot read values from your domain's session —
            so they cannot forge a valid token. Requests without it are rejected with 403.
          </p>
        </div>
        <div class="explainer__item">
          <h3 class="explainer__label">SameSite Cookies</h3>
          <p class="explainer__text">
            Setting <code>SameSite=Strict</code> on your session cookie tells the browser
            never to send it in cross-site requests. This alone can prevent most CSRF attacks
            in modern browsers, but CSRF tokens provide a defence-in-depth layer that works
            even in older browsers and edge cases.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import CsrfVulnerable from '@/components/csrf/CsrfVulnerable.vue'
import CsrfProtected from '@/components/csrf/CsrfProtected.vue'
import TransferLog from '@/components/csrf/TransferLog.vue'
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

.how-it-works {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 20px;
}

.flow {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.flow__step {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  flex: 1;
  min-width: 180px;
}

.flow__step--danger {
  border-color: rgba(255, 68, 68, 0.3);
  background: var(--accent-red-dim);
}

.flow__num {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--bg-highlight);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}

.flow__step--danger .flow__num {
  background: var(--accent-red);
  color: white;
}

.flow__text {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.flow__arrow {
  color: var(--text-muted);
  font-size: 18px;
  flex-shrink: 0;
}

.demo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 20px;
}

.explainer__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
  font-size: 12px;
  color: var(--accent-amber);
}
</style>