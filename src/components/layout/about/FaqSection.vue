<script setup lang="ts">
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'

const accordionItems = [
  {
    value: 'item-1',
    title: 'Can i use Tasker on mobile devices?',
    content: 'Yes, Tasker is fully responsive and works great on mobile devices.',
  },
  {
    value: 'item-2',
    title: 'Why create an account?',
    content:
      'Creating an account allows you to sync your tasks across devices and access your data from anywhere.',
  },
  {
    value: 'item-3',
    title: 'how does the AI assistant help?',
    content:
      'The AI assistant can help you generate tasks, track your progress, and provide insights on your productivity.',
  },
]
</script>

<template>
  <div class="flex flex-col w-full mt-8 lg:m-8 gap-2">
    <small class="rounded-full border border-primary bg-muted px-3.5 py-1.5 text-md w-fit mb-2"
      >FAQ
    </small>
    <h2 class="text-4xl font-bold">
      Frequently Asked
      <strong class="bg-linear-to-r from-primary to-accent-foreground bg-clip-text text-transparent"
        >Questions</strong
      >
    </h2>
    <p>Here are some common questions about Tasker.</p>
    <Accordion type="single" collapsible class="mt-6 lg:w-full">
      <AccordionItem
        v-for="item in accordionItems"
        :key="item.value"
        :value="item.value"
        class="px-4 py-1 border rounded-lg mb-2"
      >
        <AccordionTrigger>{{ item.title }}</AccordionTrigger>
        <AccordionContent>
          {{ item.content }}
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  </div>
</template>
