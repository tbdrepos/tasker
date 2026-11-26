<script setup lang="ts">
import type { Component } from 'vue'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

withDefaults(
  defineProps<{
    id: string
    label: string
    modelValue: string
    icon: Component
    type?: 'text' | 'email'
    autocomplete?: string
    error?: string
  }>(),
  {
    type: 'text',
    autocomplete: 'off',
    error: '',
  },
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'blur'): void
}>()
</script>

<template>
  <div class="space-y-1.5">
    <Label :for="id" class="sr-only">{{ label }}</Label>

    <div class="relative">
      <component
        :is="icon"
        class="pointer-events-none absolute left-4 top-1/2 z-10 size-5 -translate-y-1/2 text-indigo-300/80"
        aria-hidden="true"
      />
      <Input
        :id="id"
        :type="type"
        :model-value="modelValue"
        :autocomplete="autocomplete"
        :placeholder="label"
        :aria-invalid="Boolean(error)"
        :aria-describedby="error ? `${id}-error` : undefined"
        :class="[
          'h-12 rounded-xl border-white/10 bg-white/[0.03] pl-11 text-[15px] text-indigo-50 placeholder:text-slate-400 focus-visible:border-indigo-400 focus-visible:ring-indigo-500/30',
          error && 'border-rose-400/60 focus-visible:ring-rose-500/30',
        ]"
        @update:model-value="emit('update:modelValue', String($event ?? ''))"
        @blur="emit('blur')"
      />
    </div>

    <p
      v-if="error"
      :id="`${id}-error`"
      class="px-1 text-xs text-rose-300"
      role="alert"
    >
      {{ error }}
    </p>
  </div>
</template>
