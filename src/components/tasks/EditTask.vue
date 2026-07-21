<script setup lang="ts">
import { type PropType, ref } from 'vue'
import type { TaskPriorities } from '@/types/task.ts'
import { supabase } from '@/supabase/client.ts'
import { priorityStyle } from '@/types/task.ts'

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
})

const title = ref<string>(props.taskTitle)
const description = ref<string>(<string>props.taskDescription)
const priority = ref<TaskPriorities>(<'important' | 'normal' | 'trivial'>props.taskPriority)

const dialogRef = ref<HTMLDialogElement | null>(null)

// Methods to control the dialog
function showModal() {
  dialogRef.value?.showModal()
}

function close() {
  dialogRef.value?.close()
}

// Expose these methods to the parent
defineExpose({
  showModal,
  close,
})

const editTask = async () => {
  if (title.value === '' || priority.value === undefined) {
    alert('Illegal values')
    return
  }
  await supabase
    .from('tasks')
    .update({ title: title.value, description: description.value, priority: priority.value })
    .eq('id', props.taskId)
}
</script>

<template>
  <dialog ref="dialogRef">
    <button @click="close" class="edit__dialog--close-btn">✖</button>
    <form @submit.prevent="editTask">
      <label>Title:</label>
      <input type="text" v-model="title" />
      <label>Description:</label>
      <input type="text" v-model="description" />
      <label>priority:</label>
      <select v-model="priority">
        <option :value="'trivial'">trivial</option>
        <option :value="'normal'">normal</option>
        <option :value="'important'">important</option>
      </select>
      <button type="submit">Edit</button>
    </form>
  </dialog>
</template>

<style scoped>
dialog {
  background-color: var(--background-color);
  padding-top: 3rem;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
dialog::backdrop {
  background-color: rgba(0, 0, 0, 0.8);
}
dialog form {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
form button {
  height: 2.5rem;
  margin-top: 2rem !important;
}
label {
  color: var(--text-color);
}
form select,
form option {
  background-color: v-bind(priorityStyle[priority]);
  color: var(--surface-color);
}
.edit__dialog--close-btn {
  background: transparent;
  color: var(--text-color);
  max-height: fit-content;
  padding: 0.2rem 0.5rem;
  position: absolute;
  right: 1rem;
  top: 0.3rem;
}
.edit__dialog--close-btn:hover {
  background: var(--primary-color);
  color: var(--background-color);
}
</style>
