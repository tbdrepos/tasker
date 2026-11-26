<script setup lang="ts">
import AppHeader from '@/components/layout/landing/AppHeader.vue'
import ContactHero from '@/components/layout/contact/ContactHero.vue'
import ContactAssistantCTA from '@/components/layout/contact/ContactAssistantCTA.vue'
import ContactForm from '@/components/layout/contact/ContactForm.vue'
</script>

<template>
  <main class="pb-8">
    <AppHeader />
    <ContactHero />

    <div class="flex flex-col items-center p-4 lg:p-12 gap-8">
      <ContactForm />
      <ContactAssistantCTA />
    </div>
  </main>
</template>
