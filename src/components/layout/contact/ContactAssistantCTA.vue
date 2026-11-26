<script setup lang="ts">
import { ArrowRight, Bot } from '@lucide/vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

const emit = defineEmits<{
  (e: 'open-assistant'): void
}>()
</script>

<template>
  <Card
    class="h-fit w-fit relative mt-8 overflow-hidden rounded-2xl border-primary/20 bg-linear-to-r from-primary/30 to-primary/35 text-primary-foreground shadow-none"
  >
    <CardContent class="flex flex-col items-start gap-5 p-6 sm:flex-row sm:items-center">
      <span
        class="grid size-16 shrink-0 place-items-center rounded-2xl bg-linear-to-br from-accent-foreground to-violet-400 text-indigo-950 shadow-lg shadow-indigo-500/30"
        aria-hidden="true"
      >
        <Bot class="size-9" />
      </span>

      <div class="flex-1">
        <h2 class="text-xl font-semibold">Skip the wait</h2>
        <p class="mt-1 text-slate-300">
          Ask the AI Assistant. It handles most questions in seconds.
        </p>
      </div>

      <Button
        class="rounded-xl bg-linear-to-r from-primary to-violet-600 px-5 py-3 font-semibold shadow-lg shadow-primary/30 hover:brightness-110"
        @click="emit('open-assistant')"
      >
        Open chat
        <ArrowRight class="size-4" />
      </Button>
    </CardContent>
  </Card>
</template>
