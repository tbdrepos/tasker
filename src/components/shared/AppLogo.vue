<script setup lang="ts">
import { computed } from 'vue'
import { Check } from '@lucide/vue'

const props = withDefaults(
  defineProps<{
    size?: 'sm' | 'lg'
    as?: 'a' | 'div'
    href?: string
  }>(),
  {
    size: 'sm',
    as: 'div',
    href: '/',
  },
)

const markClass = computed(() => (props.size === 'lg' ? 'size-12 rounded-xl' : 'size-9 rounded-lg'))

const iconClass = computed(() => (props.size === 'lg' ? 'size-7' : 'size-5'))

const textClass = computed(() => (props.size === 'lg' ? 'text-3xl' : 'text-xl'))
</script>

<template>
  <component
    :is="as"
    :href="as === 'a' ? href : undefined"
    class="inline-flex items-center gap-2.5 font-semibold"
  >
    <span
      :class="[
        'grid shrink-0 place-items-center bg-linear-to-br from-primary to-violet-600 shadow-lg shadow-primary/30',
        markClass,
      ]"
      aria-hidden="true"
    >
      <Check :class="iconClass" :stroke-width="3.5" />
    </span>
    <span :class="textClass">Tasker</span>
  </component>
</template>
