<script setup lang="ts">
import type { Component } from 'vue'
import { Bot, Clock3, Mail, MapPin } from '@lucide/vue'
import ContactChannelCard from '@/components/shared/InfoCard.vue'

const channels: {
  icon: Component
  title: string
  description: string
}[] = [
  {
    icon: Mail,
    title: 'Email us',
    description: 'support@taskflow.app',
  },
  {
    icon: Bot,
    title: 'AI Assistant',
    description: 'Instant answers, any time of day.',
  },
  {
    icon: Clock3,
    title: 'Support hours',
    description: 'Monday to Friday, 9:00 to 18:00',
  },
  {
    icon: MapPin,
    title: 'Where we work',
    description: 'A remote-first team, worldwide.',
  },
]
</script>

<template>
  <section class="relative mt-12 grid gap-4 sm:grid-cols-2" aria-label="Contact options">
    <ContactChannelCard
      v-for="channel in channels"
      :key="channel.title"
      :icon="channel.icon"
      :title="channel.title"
      :description="channel.description"
    />
  </section>
</template>
