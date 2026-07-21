<script setup lang="ts">
import { ref } from 'vue'
import { supabase } from '../../supabase/client.ts'

const username = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')

//TODO: get user info from 'data' as session data

const addUserToSupabase = async (userName: string, email: string, password: string) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { data, error } = await supabase.auth.signUp({
    email: email,
    password: password,
    options: {
      // Optional: add extra user metadata
      data: {
        username: userName,
      },
      // Optional: specify a redirect URL after email confirmation
      //TODO: redirect to project after hosting
    },
  })

  if (error) {
    console.error(error.message)
  } else {
    console.log('User registered. Check email for confirmation link.')
    // If email confirmation is disabled, data.session and data.user will be returned immediately
  }
}

const register = async () => {
  if (!username.value || !email.value || !password.value || !passwordConfirm.value) {
    alert('all fields are required')
  } else {
    if (password.value !== passwordConfirm.value) {
      alert('password is mismatched')
    } else {
      await addUserToSupabase(username.value, email.value, password.value)
      window.location.reload()
    }
  }
}
</script>

<template>
  <form autocomplete="off" @submit.prevent="register">
    <!-- Dummy hidden fields to absorb autofill -->
    <input type="text" style="display: none" autocomplete="username" />
    <input type="password" style="display: none" autocomplete="password" />

    <!-- Actual fields -->
    <input
      type="text"
      name="user_name"
      placeholder="Username..."
      autocomplete="username"
      v-model="username"
    />

    <input
      type="email"
      name="user_email"
      placeholder="Email..."
      autocomplete="email"
      v-model="email"
    />

    <input
      type="password"
      name="new"
      placeholder="Password..."
      autocomplete="new-password"
      v-model="password"
    />

    <input
      type="password"
      name="new_confirm"
      placeholder="Confirm Password..."
      autocomplete="new-password"
      v-model="passwordConfirm"
    />

    <button type="submit">Register</button>
  </form>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}
form button {
  padding: 0.5rem;
  text-align: center;
}
</style>
