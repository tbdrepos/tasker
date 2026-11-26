<script setup lang="ts">
import type { Component } from 'vue'
import { Card, CardContent } from '@/components/ui/card'

defineProps<{
  icon: Component
  title: string
  description: string
}>()
</script>

<template>
  <Card class="rounded-2xl border-white/10 bg-white/[0.03] text-slate-300 shadow-none">
    <CardContent class="flex items-start gap-4 p-4">
      <span
        class="grid size-11 shrink-0 place-items-center rounded-full bg-accent-foreground/20 text-primary-foreground"
        aria-hidden="true"
      >
        <component :is="icon" class="size-5" />
      </span>

      <div class="min-w-0">
        <h3 class="font-semibold text-primary-foreground">{{ title }}</h3>
        <p class="mt-0.5 text-sm leading-relaxed text-muted-foreground">
          {{ description }}
        </p>
      </div>
    </CardContent>
  </Card>
</template>
