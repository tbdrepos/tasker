<script setup lang="ts">
import LoginForm from '@/components/auth/LoginForm.vue'
import { supabase } from '@/supabase/client.ts'
import { useDark, useToggle } from '@vueuse/core'

const props = defineProps({
  hasUser: {
    type: Boolean,
    required: true,
  },
  username: String,
})

const isDark = useDark()
const toggleDark = useToggle(isDark)

const signOut = async (): Promise<void> => {
  await supabase.auth.signOut()
}
</script>

<template>
  <header>
    <div class="logo-container">
      <div class="logo">Tasker</div>
    </div>

    <div class="user__info">
      <button class="dark-mode-toggle" @click="toggleDark()">{{ isDark ? '☀️' : '🌙' }}</button>
      <div v-if="!props.hasUser">
        <LoginForm />
      </div>
      <div v-else>
        <div class="user__account">
          <h3>User: {{ props.username }}</h3>
          <button class="log-out__btn" @click="signOut">Logout</button>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
header {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: fit-content;
  padding: 1rem;
}
header h1 {
  max-width: 300px;
  margin: 0 1rem;
}
.logo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 6rem; /* Adjust size as needed */
  width: 10rem;
  background-color: #f0f0f0; /* Neutral background for contrast */
  border-radius: 50%; /* Makes the container a circle */
}

.logo {
  /* Use a modern, bold font for impact */
  font-family: 'Arial', sans-serif;
  font-size: 2rem;
  font-weight: bold;
  text-align: center;

  /* Apply the gradient to the text itself */
  background: radial-gradient(circle at top left, #6a11cb 0%, #2575fc 100%);
  -webkit-background-clip: text; /* Clip the gradient to the text shape */
  background-clip: text;
  color: transparent; /* Make the text transparent to show the gradient background */
}
.user__info {
  display: flex;
  flex-direction: column;
}
.dark-mode-toggle {
  width: fit-content;
  align-self: center;
  margin-top: 1rem;
  padding: 0.8rem;
}
.user__account {
  display: flex;
  align-items: center;
  gap: 4rem;
}
.user__account h3 {
  color: var(--accent-color);
  border: 2px solid var(--accent-color);
  border-radius: 0.8rem;
  padding: 0.2rem 0.5rem;
}
.user__account .log-out__btn {
  padding: 0.5rem 1rem;
}
@media (width >= 48rem) {
  header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin: 0;
  }
  header h1 {
    margin-bottom: 0;
  }
  .user__info {
    flex-direction: row;
  }
  .dark-mode-toggle {
    padding: 0.8rem;
    margin: 0 1rem;
  }
}
@media (width >= 64rem) {
  header {
    margin: 1rem;
  }
}
</style>
