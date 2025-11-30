<script setup>
import { RouterView } from 'vue-router'
import Navigation from './components/Navigation.vue'
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <Navigation />
    <main class="container mx-auto px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>
