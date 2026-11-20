<script setup lang="ts">
import Button from '@/components/ui/button/Button.vue'
</script>
<template>
  <section class="flex items-center justify-between px-12">
    <div class="w-3xl flex flex-col items-start gap-4">
      <small
        class="text-primary-foreground font-bold bg-secondary px-4 py-1.5 rounded-xl border-2 border-accent">Smarter
        Tasks. More Focus.</small>
      <h1 class="text-6xl font-bold">
        Organize Your Work with <span class="text-primary glossy-text">AI Assistant</span>
      </h1>
      <p class="text-muted-foreground text-xl">
        A modern Kanban task manager with an integrated AI chatbot to help you stay productive.
      </p>
      <div class="flex gap-6">
        <Button>Get Started</Button>
        <Button variant="outline">Learn More</Button>
      </div>
    </div>
    <div class="w-3xl">
      <img src="@/images/landing-bg.png" alt="Hero Image" class="hidden lg:block fade-all-edges" />
    </div>
  </section>
</template>
<style lang="css" scoped>
.glossy-text {
  text-transform: uppercase;

  background:
    linear-gradient(190deg,
      rgba(255, 255, 255, 0.85) 0%,
      rgba(255, 255, 255, 0.25) 49%,
      rgba(0, 0, 0, 0.25) 50%,
      rgba(255, 255, 255, 0.15) 100%),
    var(--color-primary);

  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;

  filter: drop-shadow(0px 3px 5px rgba(0, 0, 0, 0.3));
}

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
