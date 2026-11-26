<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { CheckCircle2, Mail, MessageSquare, Send, Tag, UserRound } from '@lucide/vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Spinner } from '@/components/ui/spinner'
import { Textarea } from '@/components/ui/textarea'
import ContactTextField from '@/components/ui/ContactTextField.vue'
import TaskerLogo from '@/components/shared/AppLogo.vue'
import type { ContactFieldErrors, ContactFieldKey, ContactFormData } from '@/types/contact.types'

const emit = defineEmits<{
  (e: 'submit', payload: ContactFormData): void
  (e: 'open-assistant'): void
  (e: 'open-help-center'): void
}>()

const MAX_MESSAGE = 500

const subjects = [
  'General question',
  'Technical support',
  'Billing and plans',
  'Feature request',
  'Partnership',
] as const

const form = reactive<ContactFormData>({
  name: '',
  email: '',
  subject: '',
  message: '',
})

const errors = ref<ContactFieldErrors>({})
const status = ref<'idle' | 'sending' | 'sent'>('idle')
const firstName = computed(() => form.name.trim().split(' ')[0] || '')

function validate(): ContactFieldErrors {
  const nextErrors: ContactFieldErrors = {}

  if (form.name.trim().length < 2) {
    nextErrors.name = 'Enter your full name.'
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(form.email)) {
    nextErrors.email = 'Enter a valid email address.'
  }

  if (!form.subject) {
    nextErrors.subject = 'Choose what this is about.'
  }

  if (form.message.trim().length < 10) {
    nextErrors.message = 'Add a few more details (at least 10 characters).'
  }

  return nextErrors
}

function validateField(key: ContactFieldKey) {
  errors.value = {
    ...errors.value,
    [key]: validate()[key],
  }
}

async function onSubmit() {
  errors.value = validate()

  if (Object.keys(errors.value).some((key) => errors.value[key as ContactFieldKey])) {
    return
  }

  status.value = 'sending'

  try {
    // Replace this simulated delay with your API request.
    await new Promise((resolve) => setTimeout(resolve, 900))
    emit('submit', { ...form })
    status.value = 'sent'
  } catch {
    status.value = 'idle'
  }
}

function reset() {
  Object.assign(form, {
    name: '',
    email: '',
    subject: '',
    message: '',
  })
  errors.value = {}
  status.value = 'idle'
}
</script>

<template>
  <Card class="relative isolate w-full max-w-160 overflow-hidden rounded-3xl shadow-none">
    <CardHeader class="items-center px-6 pt-8 text-center sm:px-8">
      <TaskerLogo size="lg" />
      <CardTitle class="mt-6 text-3xl">Send Us a Message</CardTitle>
      <CardDescription class="mt-2">
        Tell us how we can help and we’ll get back to you.
      </CardDescription>
    </CardHeader>

    <CardContent class="px-6 pb-14 sm:px-8 sm:pb-16">
      <div v-if="status === 'sent'" class="mt-10 text-center" role="status">
        <span
          class="mx-auto grid size-16 place-items-center rounded-full bg-success/15 text-success ring-1 ring-success/30"
          aria-hidden="true"
        >
          <CheckCircle2 class="size-8" />
        </span>

        <h3 class="mt-5 text-xl font-semibold">Message sent</h3>
        <p class="mx-auto mt-2 max-w-xs text-muted-foreground">
          Thanks, {{ firstName }}. We’ll reply to {{ form.email }} within 24 hours.
        </p>

        <Button variant="outline" class="mx-auto mt-6 h-11 w-full max-w-xs" @click="reset">
          Send another message
        </Button>
      </div>

      <form v-else class="mt-8 space-y-4" novalidate @submit.prevent="onSubmit">
        <ContactTextField
          id="name"
          v-model="form.name"
          label="Full Name"
          autocomplete="name"
          :icon="UserRound"
          :error="errors.name"
          @blur="validateField('name')"
        />

        <ContactTextField
          id="email"
          v-model="form.email"
          label="Email Address"
          type="email"
          autocomplete="email"
          :icon="Mail"
          :error="errors.email"
          @blur="validateField('email')"
        />

        <div class="space-y-1.5">
          <Label for="subject" class="sr-only">Subject</Label>

          <div class="relative">
            <Tag
              class="pointer-events-none absolute left-4 top-1/2 size-5 -translate-y-1/2 text-muted-foreground"
              aria-hidden="true"
            />

            <Select v-model="form.subject" @update:model-value="validateField('subject')">
              <SelectTrigger
                id="subject"
                class="h-12 w-full rounded-xl pl-11 text-[15px]"
                :aria-invalid="Boolean(errors.subject)"
                :aria-describedby="errors.subject ? 'subject-error' : undefined"
                @blur="validateField('subject')"
              >
                <SelectValue placeholder="Subject" />
              </SelectTrigger>

              <SelectContent>
                <SelectItem v-for="subject in subjects" :key="subject" :value="subject">
                  {{ subject }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          <p
            v-if="errors.subject"
            id="subject-error"
            class="px-1 text-xs text-destructive"
            role="alert"
          >
            {{ errors.subject }}
          </p>
        </div>

        <div class="space-y-1.5">
          <Label for="message" class="sr-only">Message</Label>

          <div class="relative">
            <MessageSquare
              class="pointer-events-none absolute left-4 top-4 size-5 text-muted-foreground"
              aria-hidden="true"
            />
            <Textarea
              id="message"
              v-model="form.message"
              :maxlength="MAX_MESSAGE"
              rows="5"
              placeholder="How can we help?"
              class="min-h-32 resize-none rounded-xl pl-11 pt-3.5 text-[15px]"
              :aria-invalid="Boolean(errors.message)"
              :aria-describedby="errors.message ? 'message-error' : undefined"
              @blur="validateField('message')"
            />
          </div>

          <div class="flex gap-3 px-1 text-xs">
            <p v-if="errors.message" id="message-error" class="text-destructive" role="alert">
              {{ errors.message }}
            </p>
            <span class="ml-auto shrink-0 text-muted-foreground">
              {{ form.message.length }}/{{ MAX_MESSAGE }}
            </span>
          </div>
        </div>

        <Button
          type="submit"
          :disabled="status === 'sending'"
          class="h-12 w-full rounded-xl font-semibold bg-linear-to-r from-primary to-violet-600 hover:brightness-110 shadow-lg shadow-primary/30"
        >
          <Spinner v-if="status === 'sending'" class="size-5" />
          <Send v-else class="size-5" />
          {{ status === 'sending' ? 'Sending…' : 'Send Message' }}
        </Button>
      </form>
    </CardContent>

    <div
      class="absolute inset-x-0 bottom-0 -z-10 h-28 bg-linear-to-t from-primary/15 to-transparent"
      aria-hidden="true"
    />
  </Card>
</template>
