<script setup lang="ts">
import { Badge } from '@/components/ui/badge'
import ContactChannels from '@/components/layout/contact/ContactChannels.vue'
</script>

<template>
  <section
    class="flex flex-col text-center xl:text-start xl:flex-row items-center justify-between p-4 lg:p-12 lg:w-fit mx-auto"
    aria-labelledby="contact-heading"
  >
    <div class="flex flex-col items-center xl:items-start">
      <Badge
        variant="outline"
        class="rounded-full border-secondary-foreground/20 bg-secondary px-3.5 py-1.5 font-normal text-secondary-foreground/80"
      >
        We reply within 24 hours
      </Badge>

      <h1
        id="contact-heading"
        class="mt-5 text-4xl sm:text-5xl lg:w-2/3 xl:w-1/2 font-semibold leading-tight tracking-tight text-indigo-50"
      >
        Questions? Talk to
        <span class="bg-linear-to-r from-primary to-violet-500 bg-clip-text text-transparent">
          the TaskFlow team
        </span>
      </h1>

      <p class="mt-4 max-w-md text-lg leading-relaxed text-slate-400">
        Send us a message about your account, a bug, or an idea. Need an answer right now? The AI
        Assistant is always on.
      </p>
    </div>

    <ContactChannels />
  </section>
</template>
