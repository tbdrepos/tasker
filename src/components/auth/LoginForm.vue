<script setup lang="ts">
import { ref } from 'vue'
import { supabase } from '@/supabase/client.ts'

const email = ref<string>('')
const password = ref<string>('')

const signIn = async (): Promise<void> => {
  await supabase.auth.signInWithPassword({
    email: email.value,
    password: password.value,
  })
}
</script>

<template>
  <div class="login">
    <form @submit.prevent="signIn" class="login__form">
      <h3 class="login__label">Log in</h3>
      <input v-model="email" type="email" name="email" placeholder="Email" />
      <input v-model="password" type="password" name="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<style scoped>
.login__form {
  display: flex;
  flex-direction: column;
  text-align: center;
  gap: 0.8rem;
}
.login__label {
  margin: 1rem 0 0;
}

.login__form h3 {
  margin-bottom: 0.5rem;
}
@media (width >= 48rem) {
  .login__form {
    flex-direction: row;
    margin: 0;
  }
  .login__label {
    display: none;
  }
  .login__form input {
    max-width: 10rem;
  }
}
@media (width >= 80rem) {
  .login__form input {
    max-width: 16rem;
  }
}
</style>
