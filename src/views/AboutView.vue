<script setup lang="ts">
import AboutSection from '@/components/layout/about/AboutSection.vue'
import FaqSection from '@/components/layout/about/FaqSection.vue'
import ReminderSection from '@/components/layout/about/ReminderSection.vue'
import AppHeader from '@/components/layout/landing/AppHeader.vue'
</script>

<template>
  <AppHeader />
  <AboutSection />
  <div class="flex flex-col-reverse lg:flex-row w-full gap-16 px-4 lg:px-16 pb-8">
    <ReminderSection />
    <FaqSection />
  </div>
</template>
