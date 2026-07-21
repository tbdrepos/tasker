<script setup lang="ts">
const emit = defineEmits<{ (e: 'open-register'): void }>()

function openRegister() {
  emit('open-register')
}
</script>

<template>
  <section class="hero">
    <div class="hero__body">
      <h1 class="hero__title">A simple task manager</h1>
      <p class="hero__description">
        Add, edit and remove tasks through a simple interface. Have all your tasks divided into
        three clear categories.
      </p>
      <button @click="openRegister">Register</button>
    </div>
    <div class="hero__image--wrapper">
      <img src="@/images/4894122-removebg-preview.png" alt="hero-image" />
      <a
        href="https://www.freepik.com/free-vector/isometric-time-management-concept-illustrated_12281499.htm"
        >Image by pikisuperstar on Freepik
      </a>
    </div>
  </section>
</template>

<style scoped>
.hero {
  display: none;
}
@media (width >= 48rem) {
  .hero {
    display: flex;
    justify-content: space-between;
    margin: 6rem 1rem;
  }
  .hero__body {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    margin: 2rem;
  }
  .hero button {
    height: 40px;
    margin-top: 1.5rem;
  }
  .hero__image--wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 30rem;
    height: 30rem;
  }

  .hero__image--wrapper img {
    width: 400px;
    height: fit-content;
    mix-blend-mode: multiply;
  }
  .dark .hero__image--wrapper {
    border-radius: 4rem;
    background: var(--surface-color);
    padding: 0.5rem;
    box-shadow:
      0 20px 40px rgba(0, 0, 0, 0.4),
      0 0 0 1px rgba(255, 255, 255, 0.05);
  }
  .dark .hero__image--wrapper img {
    mix-blend-mode: normal;
  }
}
@media (width >= 64rem) {
  .hero {
    gap: 1rem;
  }
  .hero__body {
    flex: 1;
  }
  .hero__image--wrapper {
    flex: 1;
  }
  .hero__description {
    margin: 1.5rem 0;
  }
}
@media (width >= 96rem) {
  .hero__image--wrapper {
    margin: 0 6rem;
  }
  .hero__description {
    width: 70%;
  }
}
</style>
