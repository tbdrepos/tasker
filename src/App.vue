<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { User } from '@supabase/supabase-js'
import { supabase } from '@/supabase/client'
import TaskList from '@/components/tasks/TaskList.vue'
import AddTask from '@/components/tasks/AddTask.vue'
import RegisterForm from '@/components/auth/RegisterForm.vue'
import RegisterDialog from '@/components/auth/RegisterDialog.vue'
import AppHero from '@/components/AppHero.vue'
import AppHeader from '@/components/AppHeader.vue'
import DragSwitch from '@/components/tasks/DragSwitch.vue'
import { useLoading } from 'vue-loading-overlay'

const user = ref<User | null>(null)
const username = ref<string>('')

const registerDialog = ref<InstanceType<typeof RegisterDialog> | null>(null)

const disabled = ref<boolean>(false)

onMounted(async () => {
  //show loading screen
  const loader = useLoading().show({
    backgroundColor: '#3d36cf',
  })
  //await supabase.rpc('my_slow_function')

  //get user
  const { data } = await supabase.auth.getSession()
  user.value = data.session?.user ?? null

  //hide loading screen
  loader.hide()

  supabase.auth.onAuthStateChange((_event, session) => {
    user.value = session?.user ?? null
    //get username
    if (user.value !== null) {
      username.value = user.value.user_metadata.username
    }
  })
})

function displayRegisterDialog() {
  registerDialog.value?.showModal()
}
</script>

<template>
  <main>
    <div v-if="!user">
      <AppHeader :hasUser="false" :username="username" />
      <AppHero @open-register="displayRegisterDialog" />
      <!-- show registration form on small screens -->
      <div class="register__form">
        <hr />
        <h3>Register</h3>
        <RegisterForm />
      </div>
      <!-- show registration dialog on large screens -->
      <RegisterDialog ref="registerDialog">
        <RegisterForm />
      </RegisterDialog>
    </div>

    <div v-else>
      <AppHeader :hasUser="true" :username="username" />
      <div class="tasks__body">
        <div class="tasks__input">
          <AddTask />
          <DragSwitch label="Drag and drop:" v-model="disabled" />
        </div>
        <TaskList v-model="disabled" />
      </div>
    </div>
  </main>
</template>

<style scoped>
main {
  padding: 0;
  margin: 0;
}
.tasks__body {
  margin: 1rem;
}
.tasks__input {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.register__form {
  display: flex;
  flex-direction: column;
  text-align: center;
  width: fit-content;
  margin: auto;
}
.register__form hr {
  width: 100%;
}
@media (width >= 48rem) {
  .register__form {
    display: none;
  }
  .tasks__input {
    flex-direction: row;
    justify-content: space-between;
  }
}
@media (width >= 64rem) {
  main {
    margin: 0 100px;
  }
}
@media (width >= 96rem) {
  main {
    width: 80%;
    margin: 0 auto;
  }
}
</style>
