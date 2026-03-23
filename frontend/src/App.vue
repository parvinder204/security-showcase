<template>
  <div class="app-shell">
    <AppNav v-if="auth.isLoggedIn" />
    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppNav from '@/components/shared/AppNav.vue'

const auth = useAuthStore()

onMounted(() => {
  auth.fetchMe()
})
</script>