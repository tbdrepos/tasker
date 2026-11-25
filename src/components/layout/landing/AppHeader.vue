<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import { SquareCheck, Menu, X } from '@lucide/vue'

const menuOpen = ref(false)
</script>

<template>
  <header class="relative flex items-center justify-between gap-4 px-4 py-4 md:p-8 lg:px-24">
    <RouterLink to="/" @click="menuOpen = false">
      <div class="text-xl md:text-2xl font-bold flex items-center gap-2">
        <SquareCheck fill="var(--color-primary)" :size="32" class="md:w-10 md:h-10" />
        Tasker
      </div>
    </RouterLink>

    <!-- Desktop Nav -->
    <nav class="hidden md:block">
      <ul class="flex items-center gap-6">
        <li>
          <RouterLink
            to="/"
            class="text-lg lg:text-xl font-medium text-muted-foreground underline-offset-4 transition-colors hover:text-foreground hover:underline [&.router-link-active]:text-primary [&.router-link-active]:underline"
          >
            Home
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/about"
            class="text-lg lg:text-xl font-medium text-muted-foreground underline-offset-4 transition-colors hover:text-foreground hover:underline [&.router-link-active]:text-primary [&.router-link-active]:underline"
          >
            About
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/contact"
            class="text-lg lg:text-xl font-medium text-muted-foreground underline-offset-4 transition-colors hover:text-foreground hover:underline [&.router-link-active]:text-primary [&.router-link-active]:underline"
          >
            Contact
          </RouterLink>
        </li>
      </ul>
    </nav>

    <!-- Desktop Actions -->
    <div class="hidden md:flex items-center gap-3 lg:gap-4">
      <Button variant="outline">Sign In</Button>
      <Button variant="default">Get Started</Button>
    </div>

    <!-- Mobile Hamburger Button -->
    <Button
      variant="ghost"
      size="icon"
      class="md:hidden"
      :aria-expanded="menuOpen"
      aria-label="Toggle menu"
      @click="menuOpen = !menuOpen"
    >
      <X v-if="menuOpen" :size="24" />
      <Menu v-else :size="24" />
    </Button>

    <!-- Mobile Dropdown -->
    <div
      v-if="menuOpen"
      class="md:hidden absolute inset-x-0 top-full z-50 border-b bg-background px-4 py-6 shadow-md"
    >
      <nav class="mb-6">
        <ul class="flex flex-col gap-4">
          <li>
            <RouterLink
              to="/"
              class="block text-lg font-medium text-muted-foreground hover:text-foreground [&.router-link-active]:text-primary"
              @click="menuOpen = false"
            >
              Home
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/about"
              class="block text-lg font-medium text-muted-foreground hover:text-foreground [&.router-link-active]:text-primary"
              @click="menuOpen = false"
            >
              About
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/contact"
              class="block text-lg font-medium text-muted-foreground hover:text-foreground [&.router-link-active]:text-primary"
              @click="menuOpen = false"
            >
              Contact
            </RouterLink>
          </li>
        </ul>
      </nav>
      <div class="flex flex-col gap-2">
        <Button variant="outline" class="w-full" @click="menuOpen = false">Sign In</Button>
        <Button variant="default" class="w-full" @click="menuOpen = false">Get Started</Button>
      </div>
    </div>
  </header>
</template>
