<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { SquareCheck } from '@lucide/vue'
</script>

<template>
  <header class="flex items-center justify-between p-6 lg:px-[var(--layout-side-padding)]">
    <div class="text-2xl font-bold flex items-center">
      <SquareCheck fill="var(--color-primary)" :size="40" />

      Tasker
    </div>

    <div class="actions flex gap-4">
      <Button variant="outline">Sign In</Button>
      <Button variant="default">Get Started</Button>
    </div>
  </header>
</template>
<style lang="css" scoped></style>
