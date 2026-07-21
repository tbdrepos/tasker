<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../../supabase/client.ts'
import type { Task } from '../../types/task.ts'
import TaskColumn from '@/components/tasks/TaskColumn.vue'

const todoTasks = ref<Task[]>([])
const doingTasks = ref<Task[]>([])
const doneTasks = ref<Task[]>([])
const isLoading = ref<boolean>(false)
const errors = ref<string | null>(null)

const dragSwitch = defineModel<boolean>()

const loadTasks = async (): Promise<void> => {
  isLoading.value = true
  //await supabase.rpc('my_slow_function')

  const { data, error } = await supabase
    .from('tasks')
    .select('*')
    .order('created_at', { ascending: true })

  isLoading.value = false
  if (!error && data) {
    const tasks = data as Task[]
    todoTasks.value = tasks.filter((x) => x.status === 'todo')
    doingTasks.value = tasks.filter((x) => x.status === 'doing')
    doneTasks.value = tasks.filter((x) => x.status === 'done')
  } else {
    errors.value = error?.details
  }
}

onMounted(() => {
  loadTasks()

  //add real-time update listener
  supabase
    .channel('tasks-realtime')
    .on('postgres_changes', { event: '*', schema: 'public', table: 'tasks' }, () => {
      loadTasks()
    })
    .subscribe()
})
</script>

<template>
  <div class="tasks__container">
    <div class="tasks__container--column">
      <TaskColumn
        :tasks="todoTasks"
        status="todo"
        :isLoading="isLoading"
        :error="errors"
        v-model="dragSwitch"
      />
    </div>

    <div class="tasks__container--column">
      <TaskColumn
        :tasks="doingTasks"
        status="doing"
        :isLoading="isLoading"
        :error="errors"
        v-model="dragSwitch"
      />
    </div>

    <div class="tasks__container--column">
      <TaskColumn
        :tasks="doneTasks"
        status="done"
        :isLoading="isLoading"
        :error="errors"
        v-model="dragSwitch"
      />
    </div>
  </div>
</template>

<style scoped>
.tasks__container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
  width: 100%;
}
.tasks__container--column {
  border: 2px solid var(--primary-color);
  border-radius: 0.5rem;
}
.tasks__container--column * {
  margin: 0.5rem;
}
@media (width >= 48rem) {
  .tasks__container {
    flex-direction: row;
  }
  .tasks__container--column {
    flex: 1;
  }
}
@media (width >= 64rem) {
  .tasks__container--column {
    max-width: 35%;
  }
}
</style>
