<script setup lang="ts">
import { CircleCheckBig, Star, UserGroup } from '@lucide/vue'

const statsItems = [
  {
    key: 'item-1',
    value: '50K+',
    content: 'Active Users',
    icon: UserGroup,
  },
  {
    key: 'item-2',
    value: '99.9%',
    content: 'Uptime',
    icon: CircleCheckBig,
  },
  {
    key: 'item-3',
    value: '4.8/5',
    content: 'User Rating',
    icon: Star,
  },
]
</script>
<template>
  <section class="flex items-center justify-between p-4 lg:p-12 lg:w-fit mx-auto">
    <div
      class="pointer-events-none absolute lg:hidden right-0 top-30 h-60 w-40 rounded-full bg-primary/40 blur-3xl"
      aria-hidden="true"
    />
    <div
      class="w-full lg:w-3xl flex flex-col items-center text-center lg:text-start lg:items-start justify-center gap-8"
    >
      <small class="rounded-full border border-primary bg-muted px-3.5 py-1.5 text-md w-fit"
        >About Tasker</small
      >
      <div class="flex flex-col items-center lg:items-start gap-1">
        <h1 class="text-4xl sm:text-5xl font-bold">
          About
          <span
            class="bg-linear-to-r from-primary to-accent-foreground bg-clip-text text-transparent"
            >Us</span
          >
        </h1>
      </div>
      <p class="text-muted-foreground text-xl">
        Tasker is more than just a task manager. It's your personal productivity companion, designed
        to help you organize, prioritize, and accomplish everything you need to get done with the
        power of AI.
      </p>
      <div class="flex divide-x gap-6">
        <div class="flex items-center gap-2 p-4" v-for="item in statsItems" :key="item.key">
          <component :is="item.icon" class="w-6 h-6 text-primary" />
          <div class="flex flex-col">
            <h6 class="font-bold">{{ item.value }}</h6>
            <p class="text-muted-foreground">{{ item.content }}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="hidden lg:block lg:max-w-2xl 2xl:max-w-3xl">
      <img src="@/images/landing-bg.png" alt="Hero Image" class="fade-all-edges" />
    </div>
  </section>
</template>
<style lang="css" scoped>
.fade-all-edges {
  /* Standard syntax */
  mask-image:
    linear-gradient(to right, transparent, black 15%, black 85%, transparent),
    linear-gradient(to bottom, transparent, black 15%, black 85%, transparent);
  mask-composite: intersect;

  /* Safari & older WebKit support */
  -webkit-mask-image:
    linear-gradient(to right, transparent, black 15%, black 85%, transparent),
    linear-gradient(to bottom, transparent, black 15%, black 85%, transparent);
  -webkit-mask-composite: source-in;
}
</style>
