<script setup lang="ts">
import { computed, h, reactive, ref, type FunctionalComponent } from 'vue'

/* ---------- Types ---------- */
interface ContactForm {
  name: string
  email: string
  subject: string
  message: string
}
type FieldKey = keyof ContactForm
type FieldErrors = Partial<Record<FieldKey, string>>

const emit = defineEmits<{ (e: 'submit', payload: ContactForm): void }>()

/* ---------- Icons (inline, no extra dependency) ---------- */
const icons = {
  user: 'M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2M12 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8z',
  mail: 'M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zM22 7l-10 6L2 7',
  tag: 'M12 2H2v10l9.29 9.29a1 1 0 0 0 1.42 0l6.58-6.58a1 1 0 0 0 0-1.42L12 2zM7 7h.01',
  message: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z',
  pin: 'M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0zM12 7a3 3 0 1 0 0 6 3 3 0 0 0 0-6z',
  clock: 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM12 6v6l4 2',
  send: 'M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z',
  bot: 'M12 8V4H8M4 8h16a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2zM2 14h2M20 14h2M15 13v2M9 13v2',
  help: 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3M12 17h.01',
  check: 'M20 6L9 17l-5-5',
  chevron: 'M6 9l6 6 6-6',
  arrow: 'M5 12h14M12 5l7 7-7 7',
} as const
type IconName = keyof typeof icons

const Icon: FunctionalComponent<{ name: IconName }> = (props) =>
  h(
    'svg',
    {
      viewBox: '0 0 24 24',
      fill: 'none',
      stroke: 'currentColor',
      'stroke-width': 1.8,
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round',
      'aria-hidden': 'true',
    },
    [h('path', { d: icons[props.name] })],
  )
Icon.props = ['name']

/* ---------- Content ---------- */
const navLinks = ['Features', 'About', 'Pricing', 'Contact']

const channels: { icon: IconName; title: string; text: string }[] = [
  { icon: 'mail', title: 'Email us', text: 'support@taskflow.app' },
  { icon: 'bot', title: 'AI Assistant', text: 'Instant answers, any time of day.' },
  { icon: 'clock', title: 'Support hours', text: 'Monday to Friday, 9:00 to 18:00' },
  { icon: 'pin', title: 'Where we work', text: 'A remote-first team, worldwide.' },
]

const subjects = [
  'General question',
  'Technical support',
  'Billing and plans',
  'Feature request',
  'Partnership',
] as const

const textFields: {
  key: 'name' | 'email'
  label: string
  type: string
  icon: IconName
  autocomplete: string
}[] = [
  { key: 'name', label: 'Full Name', type: 'text', icon: 'user', autocomplete: 'name' },
  { key: 'email', label: 'Email Address', type: 'email', icon: 'mail', autocomplete: 'email' },
]

/* ---------- Form state ---------- */
const MAX_MESSAGE = 500
const form = reactive<ContactForm>({ name: '', email: '', subject: '', message: '' })
const errors = ref<FieldErrors>({})
const status = ref<'idle' | 'sending' | 'sent'>('idle')
const firstName = computed(() => form.name.trim().split(' ')[0])

function validate(): FieldErrors {
  const e: FieldErrors = {}
  if (form.name.trim().length < 2) e.name = 'Enter your full name.'
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(form.email)) e.email = 'Enter a valid email address.'
  if (!form.subject) e.subject = 'Choose what this is about.'
  if (form.message.trim().length < 10)
    e.message = 'Add a few more details (at least 10 characters).'
  return e
}

function validateField(key: FieldKey) {
  errors.value = { ...errors.value, [key]: validate()[key] }
}

async function onSubmit() {
  errors.value = validate()
  if (Object.keys(errors.value).length) return
  status.value = 'sending'
  try {
    // TODO: replace with your API call, e.g. await api.post('/contact', form)
    await new Promise((resolve) => setTimeout(resolve, 900))
    emit('submit', { ...form })
    status.value = 'sent'
  } catch {
    status.value = 'idle'
  }
}

function reset() {
  Object.assign(form, { name: '', email: '', subject: '', message: '' })
  errors.value = {}
  status.value = 'idle'
}

/* ---------- Shared Tailwind class strings ---------- */
const wrap =
  'relative flex rounded-xl border bg-white/[0.04] transition focus-within:border-indigo-400 focus-within:ring-2 focus-within:ring-indigo-500/30'
const control =
  'w-full bg-transparent py-3.5 pl-12 pr-4 text-[15px] text-indigo-50 outline-none placeholder:text-slate-400'
const outlineBtn =
  'flex w-full items-center justify-center gap-3 rounded-xl border border-white/10 bg-white/[0.03] py-3 text-[15px] font-medium text-indigo-50 transition hover:border-indigo-400/50 hover:bg-white/[0.07] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400'
</script>

<template>
  <div class="min-h-screen bg-[#060615] p-4 font-sans text-slate-300 antialiased sm:p-6">
    <div class="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[1.35fr_1fr]">
      <!-- ============ Left: intro ============ -->
      <section
        class="relative overflow-hidden rounded-3xl border border-indigo-400/20 bg-gradient-to-b from-[#0c0c2b] to-[#080819] p-6 sm:p-8"
      >
        <div
          class="pointer-events-none absolute -right-24 top-24 h-80 w-80 rounded-full bg-indigo-600/30 blur-3xl"
          aria-hidden="true"
        />

        <header class="relative flex items-center justify-between gap-4">
          <a href="/" class="flex items-center gap-2.5 text-xl font-semibold text-indigo-50">
            <span
              class="grid h-9 w-9 place-items-center rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 text-white shadow-lg shadow-indigo-600/40"
            >
              <Icon name="check" class="h-5 w-5" />
            </span>
            TaskFlow
          </a>
          <nav class="hidden items-center gap-7 text-sm md:flex" aria-label="Main">
            <a
              v-for="link in navLinks"
              :key="link"
              href="#"
              :aria-current="link === 'Contact' ? 'page' : undefined"
              :class="link === 'Contact' ? 'text-indigo-300' : 'text-slate-300 hover:text-white'"
              >{{ link }}</a
            >
          </nav>
          <a
            href="#"
            class="rounded-lg border border-white/20 px-4 py-2 text-sm font-medium text-indigo-50 transition hover:border-indigo-400/60"
            >Login</a
          >
        </header>

        <div class="relative mt-14 max-w-xl">
          <span
            class="inline-block rounded-full border border-indigo-400/30 bg-indigo-500/10 px-3.5 py-1.5 text-xs text-indigo-200"
          >
            We reply within 24 hours
          </span>
          <h1
            class="mt-5 text-4xl font-semibold leading-tight tracking-tight text-indigo-50 sm:text-5xl"
          >
            Questions? Talk to
            <span class="bg-linear-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent"
              >the TaskFlow team</span
            >
          </h1>
          <p class="mt-4 max-w-md text-lg leading-relaxed text-slate-400">
            Send us a message about your account, a bug, or an idea. Need an answer right now? The
            AI Assistant is always on.
          </p>
        </div>

        <ul class="relative mt-12 grid gap-4 sm:grid-cols-2">
          <li
            v-for="c in channels"
            :key="c.title"
            class="flex items-start gap-4 rounded-2xl border border-white/10 bg-white/[0.03] p-4"
          >
            <span
              class="grid h-11 w-11 shrink-0 place-items-center rounded-full bg-indigo-500/20 text-indigo-300"
            >
              <Icon :name="c.icon" class="h-5 w-5" />
            </span>
            <div>
              <h3 class="font-semibold text-indigo-50">{{ c.title }}</h3>
              <p class="mt-0.5 text-sm text-slate-400">{{ c.text }}</p>
            </div>
          </li>
        </ul>

        <div
          class="relative mt-8 flex flex-col items-start gap-5 overflow-hidden rounded-2xl border border-indigo-400/20 bg-gradient-to-r from-indigo-950 to-indigo-800/60 p-6 sm:flex-row sm:items-center"
        >
          <span
            class="grid h-16 w-16 shrink-0 place-items-center rounded-2xl bg-gradient-to-br from-indigo-300 to-violet-400 text-indigo-950 shadow-lg shadow-indigo-500/30"
          >
            <Icon name="bot" class="h-9 w-9" />
          </span>
          <div class="flex-1">
            <h2 class="text-xl font-semibold text-indigo-50">Skip the wait</h2>
            <p class="mt-1 text-slate-300">
              Ask the AI Assistant. It handles most questions in seconds.
            </p>
          </div>
          <button
            type="button"
            class="flex items-center gap-2 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/30 transition hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-300"
          >
            Open chat <Icon name="arrow" class="h-4 w-4" />
          </button>
        </div>
      </section>

      <!-- ============ Right: form ============ -->
      <section
        class="relative overflow-hidden rounded-3xl border border-indigo-400/20 bg-[#0a0a22] p-6 pb-32 sm:p-8 sm:pb-32"
      >
        <div class="relative text-center">
          <div class="inline-flex items-center gap-3 text-3xl font-semibold text-indigo-50">
            <span
              class="grid h-12 w-12 place-items-center rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 text-white shadow-lg shadow-indigo-600/40"
            >
              <Icon name="check" class="h-7 w-7" />
            </span>
            TaskFlow
          </div>
          <h2 class="mt-6 text-3xl font-semibold text-indigo-50">Send Us a Message</h2>
          <p class="mt-2 text-slate-400">Tell us how we can help and we’ll get back to you.</p>
        </div>

        <!-- Success state -->
        <div v-if="status === 'sent'" class="relative mt-10 text-center" role="status">
          <span
            class="mx-auto grid h-16 w-16 place-items-center rounded-full bg-emerald-500/15 text-emerald-300 ring-1 ring-emerald-400/30"
          >
            <Icon name="check" class="h-8 w-8" />
          </span>
          <h3 class="mt-5 text-xl font-semibold text-indigo-50">Message sent</h3>
          <p class="mx-auto mt-2 max-w-xs text-slate-400">
            Thanks, {{ firstName }}. We’ll reply to {{ form.email }} within 24 hours.
          </p>
          <button type="button" :class="[outlineBtn, 'mx-auto mt-6 max-w-xs']" @click="reset">
            Send another message
          </button>
        </div>

        <!-- Form -->
        <form v-else class="relative mt-8 space-y-4" novalidate @submit.prevent="onSubmit">
          <div v-for="f in textFields" :key="f.key">
            <label :for="f.key" class="sr-only">{{ f.label }}</label>
            <div
              :class="[
                wrap,
                'items-center',
                errors[f.key] ? 'border-rose-400/60' : 'border-white/10',
              ]"
            >
              <Icon
                :name="f.icon"
                class="pointer-events-none absolute left-4 h-5 w-5 text-indigo-300/80"
              />
              <input
                :id="f.key"
                v-model="form[f.key]"
                :type="f.type"
                :autocomplete="f.autocomplete"
                :placeholder="f.label"
                :aria-invalid="!!errors[f.key]"
                :aria-describedby="errors[f.key] ? `${f.key}-error` : undefined"
                :class="control"
                @blur="validateField(f.key)"
              />
            </div>
            <p
              v-if="errors[f.key]"
              :id="`${f.key}-error`"
              role="alert"
              class="mt-1.5 px-1 text-xs text-rose-300"
            >
              {{ errors[f.key] }}
            </p>
          </div>

          <!-- Subject -->
          <div>
            <label for="subject" class="sr-only">Subject</label>
            <div
              :class="[
                wrap,
                'items-center',
                errors.subject ? 'border-rose-400/60' : 'border-white/10',
              ]"
            >
              <Icon
                name="tag"
                class="pointer-events-none absolute left-4 h-5 w-5 text-indigo-300/80"
              />
              <select
                id="subject"
                v-model="form.subject"
                :aria-invalid="!!errors.subject"
                :aria-describedby="errors.subject ? 'subject-error' : undefined"
                :class="[
                  control,
                  'appearance-none',
                  form.subject ? 'text-indigo-50' : 'text-slate-400',
                ]"
                @change="validateField('subject')"
                @blur="validateField('subject')"
              >
                <option value="" disabled>Subject</option>
                <option
                  v-for="s in subjects"
                  :key="s"
                  :value="s"
                  class="bg-[#0a0a22] text-indigo-50"
                >
                  {{ s }}
                </option>
              </select>
              <Icon
                name="chevron"
                class="pointer-events-none absolute right-4 h-5 w-5 text-slate-400"
              />
            </div>
            <p
              v-if="errors.subject"
              id="subject-error"
              role="alert"
              class="mt-1.5 px-1 text-xs text-rose-300"
            >
              {{ errors.subject }}
            </p>
          </div>

          <!-- Message -->
          <div>
            <label for="message" class="sr-only">Message</label>
            <div
              :class="[
                wrap,
                'items-start',
                errors.message ? 'border-rose-400/60' : 'border-white/10',
              ]"
            >
              <Icon
                name="message"
                class="pointer-events-none absolute left-4 top-4 h-5 w-5 text-indigo-300/80"
              />
              <textarea
                id="message"
                v-model="form.message"
                rows="5"
                :maxlength="MAX_MESSAGE"
                placeholder="How can we help?"
                :aria-invalid="!!errors.message"
                :aria-describedby="errors.message ? 'message-error' : undefined"
                :class="[control, 'resize-none']"
                @blur="validateField('message')"
              />
            </div>
            <div class="mt-1.5 flex justify-between gap-3 px-1 text-xs">
              <p v-if="errors.message" id="message-error" role="alert" class="text-rose-300">
                {{ errors.message }}
              </p>
              <span v-else />
              <span class="text-slate-500">{{ form.message.length }}/{{ MAX_MESSAGE }}</span>
            </div>
          </div>

          <button
            type="submit"
            :disabled="status === 'sending'"
            class="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 py-3.5 font-semibold text-white shadow-lg shadow-indigo-600/30 transition hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-300 disabled:cursor-not-allowed disabled:opacity-70"
          >
            <svg
              v-if="status === 'sending'"
              class="h-5 w-5 animate-spin"
              viewBox="0 0 24 24"
              fill="none"
              aria-hidden="true"
            >
              <circle
                cx="12"
                cy="12"
                r="9"
                stroke="currentColor"
                stroke-opacity=".3"
                stroke-width="3"
              />
              <path
                d="M21 12a9 9 0 0 0-9-9"
                stroke="currentColor"
                stroke-width="3"
                stroke-linecap="round"
              />
            </svg>
            <Icon v-else name="send" class="h-5 w-5" />
            {{ status === 'sending' ? 'Sending…' : 'Send Message' }}
          </button>

          <div class="flex items-center gap-4 text-sm text-slate-400" role="separator">
            <span class="h-px flex-1 bg-white/10" />or<span class="h-px flex-1 bg-white/10" />
          </div>

          <button type="button" :class="outlineBtn">
            <Icon name="bot" class="h-5 w-5 text-indigo-300" /> Chat with AI Assistant
          </button>
          <button type="button" :class="outlineBtn">
            <Icon name="help" class="h-5 w-5 text-indigo-300" /> Browse the Help Center
          </button>

          <p class="pt-2 text-center text-slate-300">
            Don’t have an account?
            <a href="#" class="font-medium text-indigo-400 hover:text-indigo-300">Register</a>
          </p>
        </form>

        <svg
          class="pointer-events-none absolute inset-x-0 bottom-0 h-28 w-full text-indigo-700/50"
          viewBox="0 0 400 100"
          preserveAspectRatio="none"
          fill="currentColor"
          aria-hidden="true"
        >
          <path d="M0 60C80 10 160 30 240 65S360 90 400 40V100H0Z" />
        </svg>
      </section>
    </div>
  </div>
</template>
