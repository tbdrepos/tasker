<script setup lang="ts">
import { ref } from 'vue'

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
</script>

<template>
  <dialog ref="dialogRef">
    <button @click="close" class="register__dialog--close-btn">✖</button>
    <slot />
  </dialog>
</template>

<style scoped>
dialog {
  padding-top: 3rem;
  background-color: var(--background-color);
}
dialog::backdrop {
  background-color: rgba(0, 0, 0, 0.8);
}
.register__dialog--close-btn {
  background: transparent;
  color: var(--text-color);
  max-height: fit-content;
  padding: 0.2rem 0.5rem;
  position: absolute;
  right: 1rem;
  top: 0.3rem;
}
.register__dialog--close-btn:hover {
  background: var(--primary-color);
  color: var(--background-color);
}
</style>
