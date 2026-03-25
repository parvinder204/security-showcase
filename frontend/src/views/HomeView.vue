<template>
  <div class="home">
    <div class="home__hero container">
      <div class="home__eyebrow">
        <span class="badge badge--red">Live Vulnerability Lab</span>
      </div>

      <h1 class="home__title">
        Web Security<br />
        <span class="home__title-accent">Under the Hood</span>
      </h1>

      <p class="home__subtitle">
        An interactive walkthrough of CSRF and XSS attacks — how they work,
        how attackers exploit them, and how you defend against them.
        All demos run against a real FastAPI backend.
      </p>

      <div class="home__actions" v-if="!auth.isLoggedIn">
        <RouterLink to="/login" class="btn btn--safe home__cta">
          Login to Start →
        </RouterLink>
      </div>
      <div class="home__actions" v-else>
        <RouterLink to="/csrf" class="btn btn--danger">Explore CSRF →</RouterLink>
        <RouterLink to="/xss" class="btn btn--safe">Explore XSS →</RouterLink>
      </div>
    </div>

    <div class="home__cards container">
      <div class="home__card home__card--csrf" @click="router.push(auth.isLoggedIn ? '/csrf' : '/login')">
        <div class="home__card-tag badge badge--red">CSRF</div>
        <h2 class="home__card-title">Cross-Site Request Forgery</h2>
        <p class="home__card-desc">
          Exploit how browsers automatically attach cookies to outgoing requests.
          Watch a forged bank transfer succeed — then see why CSRF tokens stop it cold.
        </p>
        <div class="home__card-footer">
          <span class="home__card-threat">Threat: Unauthorized Actions</span>
          <span class="home__card-arrow">→</span>
        </div>
      </div>

      <div class="home__card home__card--xss" @click="router.push(auth.isLoggedIn ? '/xss' : '/login')">
        <div class="home__card-tag badge badge--amber">XSS</div>
        <h2 class="home__card-title">Cross-Site Scripting</h2>
        <p class="home__card-desc">
          Inject malicious JavaScript through a comment field that gets stored in the database
          and executed in every victim's browser. Then see how sanitization neutralizes it.
        </p>
        <div class="home__card-footer">
          <span class="home__card-threat">Threat: Session Hijacking</span>
          <span class="home__card-arrow">→</span>
        </div>
      </div>
    </div>

    <div class="home__info container">
      <div class="home__info-grid">
        <div class="home__info-item">
          <span class="home__info-label">Backend</span>
          <span class="home__info-value">FastAPI + Python</span>
        </div>
        <div class="home__info-item">
          <span class="home__info-label">Frontend</span>
          <span class="home__info-value">Vue 3 + Vite</span>
        </div>
        <div class="home__info-item">
          <span class="home__info-label">Auth</span>
          <span class="home__info-value">Session Cookies</span>
        </div>
        <div class="home__info-item">
          <span class="home__info-label">Sanitizer</span>
          <span class="home__info-value">bleach (Python)</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
</script>

<style scoped>
.home {
  padding-bottom: 80px;
}

.home__hero {
  padding-top: 100px;
  padding-bottom: 80px;
  text-align: center;
}

.home__eyebrow {
  margin-bottom: 24px;
}

.home__title {
  font-size: clamp(48px, 8vw, 88px);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.05;
  margin-bottom: 24px;
  color: var(--text-primary);
}

.home__title-accent {
  color: var(--accent-red);
}

.home__subtitle {
  max-width: 560px;
  margin: 0 auto 40px;
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.7;
}

.home__actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.home__cta {
  padding: 14px 32px;
  font-size: 15px;
}

.home__cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.home__card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  padding: 32px;
  cursor: pointer;
  transition: all 0.22s ease;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.home__card:hover {
  transform: translateY(-2px);
  border-color: var(--border-default);
}

.home__card--csrf:hover {
  border-color: rgba(255, 68, 68, 0.35);
  box-shadow: 0 8px 40px rgba(255, 68, 68, 0.1);
}

.home__card--xss:hover {
  border-color: rgba(255, 170, 0, 0.35);
  box-shadow: 0 8px 40px rgba(255, 170, 0, 0.1);
}

.home__card-title {
  font-size: 22px;
  font-weight: 700;
}

.home__card-desc {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.7;
  flex: 1;
}

.home__card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
  padding-top: 16px;
  border-top: 1px solid var(--border-subtle);
}

.home__card-threat {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.home__card-arrow {
  color: var(--text-muted);
  transition: all var(--transition);
}

.home__card:hover .home__card-arrow {
  color: var(--text-primary);
  transform: translateX(4px);
}

.home__info {
  border-top: 1px solid var(--border-subtle);
  padding-top: 40px;
}

.home__info-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  text-align: center;
}

.home__info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.home__info-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  font-weight: 700;
}

.home__info-value {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 700;
  font-family: var(--font-display);
}
</style>