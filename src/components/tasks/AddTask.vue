<script setup lang="ts">
import { ref } from 'vue'
import { supabase } from '@/supabase/client.ts'
import type { TaskPriorities, TaskStatus } from '@/types/task.ts'
import { priorityStyle } from '@/types/task.ts'

const title = ref<string>('')
const description = ref<string>('')
const priority = ref<TaskPriorities>('trivial')

const addTask = async (): Promise<void> => {
  if (!title.value.trim()) return

  await supabase.from('tasks').insert({
    title: title.value,
    description: description.value,
    priority: priority.value,
    status: 'todo' as TaskStatus,
  })

  title.value = ''
  description.value = ''
  priority.value = 'trivial'
}
</script>

<template>
  <div>
    <h3>Add a new task:</h3>
    <div class="task__form">
      <input v-model="title" type="text" placeholder="New task..." />
      <input v-model="description" type="text" placeholder="description..." />
      <select v-model="priority">
        <option :value="'trivial'">trivial</option>
        <option :value="'normal'">normal</option>
        <option :value="'important'">important</option>
      </select>
      <button @click="addTask">Add</button>
    </div>
  </div>
</template>
<style scoped>
h3 {
  margin: 0.5rem 0;
}
.task__form {
  margin-bottom: 1rem;
}
.task__form select,
.task__form option {
  background-color: v-bind(priorityStyle[priority]);
}
.dark .task__form option,
.dark .task__form select {
  color: var(--background-color);
}
</style>
