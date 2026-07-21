<script setup lang="ts">
const disabled = defineModel<boolean>()

defineProps({
  label: String,
})

const disable = () => {
  disabled.value = !disabled.value
}
</script>

<template>
  <label class="switch-container">
    <span v-if="label">{{ label }}</span>
    <div class="switch">
      <input type="checkbox" role="switch" />
      <span class="slider" @click="disable"></span>
    </div>
  </label>
</template>

<style scoped>
.switch-container {
  display: flex;
  gap: 1rem;
  align-items: center;
}
.switch-container span {
  font-size: 1.2rem;
  font-weight: bold;
}
/* The switch container (label) */
.switch {
  position: relative;
  display: inline-block;
  width: 60px; /* Adjust width as needed */
  height: 34px; /* Adjust height as needed */
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider (span) - the track */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: 0.4s;
  transition: 0.4s;
  border-radius: 34px; /* Makes it rounded */
}

/* The slider (span) - the thumb */
.slider:before {
  position: absolute;
  content: '';
  height: 26px; /* Adjust size relative to height */
  width: 26px; /* Adjust size relative to width */
  left: 4px; /* Spacing from the edge */
  bottom: 4px; /* Spacing from the edge */
  background-color: white;
  -webkit-transition: 0.4s;
  transition: 0.4s;
  border-radius: 50%; /* Makes it circular */
}

/* Change background color when checked */
input:checked + .slider {
  background-color: var(--primary-color);
}

/* Move the thumb when checked */
input:checked + .slider:before {
  -webkit-transform: translateX(26px); /* Move by the thumb width + spacing */
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}
</style>
