<script setup lang="ts">
import TaskCard from '@/components/tasks/TaskCard.vue'
import type { Task, TaskStatus } from '@/types/task.ts'
import { supabase } from '@/supabase/client.ts'
import { ref, watch } from 'vue'
import type { SortableEvent } from 'sortablejs'
import Draggable from 'vuedraggable'

interface DraggableHTMLElement extends HTMLElement {
  __draggable_context: {
    element: Task
    index: number
    futureIndex: number
  }
}

const dragSwitch = defineModel<boolean>()

const props = defineProps<{
  tasks: Task[]
  status: TaskStatus
  isLoading: boolean
  error: string | null
}>()

const columnTasks = ref<Task[]>([])

watch(
  () => props.tasks,
  (newTasks) => {
    columnTasks.value = [...newTasks]
  },
  { immediate: true },
)

const statusInfo = {
  todo: { title: 'To Do:', update: 'doing' },
  doing: { title: 'Doing:', update: 'done' },
  done: { title: 'Done', update: '' },
}

const updateStatus = async (id: string, status: TaskStatus): Promise<void> => {
  await supabase.from('tasks').update({ status }).eq('id', id)
}

const onDragEnd = async (evt: SortableEvent) => {
  const task: Task = (evt.item as DraggableHTMLElement).__draggable_context.element
  const newStatus = evt.to.dataset.column as TaskStatus

  if (!newStatus || task.status === newStatus) return

  const { error } = await supabase.from('tasks').update({ status: newStatus }).eq('id', task.id)

  if (error) {
    alert('Failed to update task:' + error)
  }
}

const cancelColumnTasks = async () => {
  const confirmDeleteTask = confirm(`Are you sure you want to delete all ${props.status} tasks?`)
  if (!confirmDeleteTask) return
  await supabase.from('tasks').delete().eq('status', props.status)
}
</script>

<template>
  <div v-if="props.isLoading">
    <div class="spinner"></div>
  </div>
  <div v-else-if="props.error != null">
    <h1>error</h1>
  </div>
  <div v-else>
    <h2 class="column__header">
      {{ statusInfo[props.status].title }}
      <button @click="cancelColumnTasks()" aria-label="Delete column" title="Delete column">
        ✖
      </button>
    </h2>

    <!-- if drag and drop is enabled, hide update button and use draggable instead -->
    <div v-if="dragSwitch">
      <Draggable
        v-model="columnTasks"
        group="tasks"
        item-key="id"
        :data-column="props.status"
        @end="onDragEnd"
        class="tasks__column"
      >
        <template #item="{ element }">
          <TaskCard
            :taskId="element.id"
            :task-title="element.title"
            :task-description="element.description"
            :task-priority="element.priority"
            :task-created-at="element.created_at"
          />
        </template>
      </Draggable>
    </div>

    <div v-else class="tasks__column">
      <div v-for="t in columnTasks" :key="t.id" class="task__row">
        <TaskCard
          :taskId="t.id"
          :task-title="t.title"
          :task-description="t.description"
          :task-priority="t.priority"
          :task-created-at="t.created_at"
        />
        <div v-if="statusInfo[props.status].update !== ''" class="column__update">
          <button
            @click="updateStatus(t.id, statusInfo[props.status].update as TaskStatus)"
            class="column__update--btn"
          ></button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tasks__column {
  display: flex;
  flex-direction: column;
}
.task__row {
  display: flex;
  justify-content: space-evenly;
}
.tasks__container--column h2 {
  border-bottom: 2px solid var(--primary-color);
  padding: 0.5rem;
}
.column__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.column__header button {
  background: var(--background-color);
  color: red;
  border: 1px solid var(--text-color);
  border-radius: 10rem;
  padding: 0.2rem 0.6rem;
  font-weight: 600;
}
.column__header button:hover {
  background: red;
  color: var(--background-color);
  border-color: red;
}
.column__update--btn::before {
  content: '↘';
}
.column__update {
  margin: 0 !important;
  padding: 0;
  align-self: center;
  width: fit-content;
}
.column__update--btn {
  margin: 0 !important;
}
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #3498db; /* Blue color */
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 10px auto;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
@media (width >= 48rem) {
  .column__update--btn::before {
    content: '→';
  }
}
</style>
