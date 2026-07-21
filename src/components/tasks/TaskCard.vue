<script setup lang="ts">
import type { TaskPriorities } from '@/types/task.ts'
import { type PropType, ref } from 'vue'
import { supabase } from '@/supabase/client.ts'
import { priorityStyle } from '@/types/task.ts'
import EditTask from '@/components/tasks/EditTask.vue'

const props = defineProps({
  taskId: {
    type: String,
    required: true,
  },
  taskTitle: {
    type: String,
    required: true,
  },
  taskDescription: String,
  taskPriority: String as PropType<TaskPriorities>,
  taskCreatedAt: String,
})

const editTaskDialog = ref<InstanceType<typeof EditTask> | null>(null)

const timeOptions = {
  day: '2-digit',
  month: '2-digit',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
  hour12: false, // Use 24-hour format
  timeZoneName: 'short', // e.g., "CET"
} as Intl.DateTimeFormatOptions

const formattedDate = ref(
  new Intl.DateTimeFormat(navigator.language, timeOptions).format(
    new Date(props.taskCreatedAt as string),
  ),
)

const cancelTask = async () => {
  const confirmDeleteTask = confirm(`Are you sure you want to delete task?`)
  if (!confirmDeleteTask) return
  await supabase.from('tasks').delete().eq('id', props.taskId)
}

const showEditDialog = () => {
  editTaskDialog.value?.showModal()
}
</script>

<template>
  <div class="task__card">
    <div class="card__header">
      <h3>{{ props.taskTitle }}</h3>
      <div class="card__edit">
        <button
          @click="showEditDialog"
          class="card__edit--update"
          aria-label="Edit task"
          title="Edit task"
        >
          ✏️
        </button>
        <button
          @click="cancelTask"
          class="card__edit--delete"
          aria-label="Delete task"
          title="Delete task"
        >
          ✖
        </button>
      </div>
    </div>
    <p>{{ props.taskDescription }}</p>
    <small>{{ formattedDate }}</small>
    <EditTask
      ref="editTaskDialog"
      :taskId="props.taskId"
      :taskTitle="props.taskTitle"
      :taskDescription="props.taskDescription"
      :taskPriority="props.taskPriority"
      class="editTaskDialog"
    />
  </div>
</template>

<style scoped>
.task__card {
  background: v-bind(priorityStyle[taskPriority]);
  color: #1d1d20;
  padding: 0.5rem;
  border-radius: 1rem;
  overflow-wrap: anywhere;
  width: 100%;
  align-self: center;
}
.card__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.card__header h3 {
  align-self: center;
}
p {
  margin: 0.8rem 0.5rem !important;
}
.card__edit {
  display: flex;
  gap: 1rem;
}
.card__edit--update {
  border: 1px solid var(--accent-color);
  border-radius: 10rem;
  background-color: color-mix(in srgb, gray 30%, transparent);
  padding: 0.3rem;
}
.card__edit--update:hover {
  background-color: color-mix(in srgb, gray 90%, transparent);
}
.card__edit--delete {
  background: var(--background-color);
  color: red;
  border: 1px solid var(--text-color);
  border-radius: 10rem;
  padding: 0.4rem 0.6rem;
  font-weight: 600;
}
.card__edit--delete:hover {
  background: red;
  color: var(--background-color);
  border-color: red;
}
</style>
