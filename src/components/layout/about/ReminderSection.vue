<script setup lang="ts">
import Button from '@/components/ui/button/Button.vue'
import { CircleCheck, Goal, ArrowRight } from '@lucide/vue'

const goals = [
  { key: 'item-1', value: 'Boost your productivity' },
  { key: 'item-2', value: 'Stay organized effortlessly' },
  { key: 'item-3', value: 'Achieve your goals' },
]
</script>

<template>
  <article
    class="relative isolate overflow-hidden rounded-2xl border border-primary/20 bg-card p-8 w-full max-w-md flex flex-col gap-5 shadow-xl before:content-[''] before:absolute before:inset-0 before:-z-10 before:bg-(image:--wavy-img) before:bg-no-repeat before:bg-cover before:-scale-x-100"
  >
    <Goal class="w-16 h-16 text-primary" />
    <h4 class="text-2xl font-bold">Our Mission</h4>
    <p class="text-lg">
      To make productivity simple, smart and enjoyable for everyone. by combining powerful task
      management with intelligent assistance.
    </p>
    <ul>
      <li
        v-for="goal in goals"
        :key="goal.key"
        class="mt-2 flex gap-2 text-muted-foreground text-md"
      >
        <CircleCheck class="w-5 h-5" :fill="'var(--color-primary)'" />
        {{ goal.value }}
      </li>
    </ul>
    <Button class="w-fit">
      Start Your Journey
      <ArrowRight />
    </Button>
  </article>
</template>
