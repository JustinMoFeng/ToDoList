<!-- App.vue -->
<template>
  <div id="app">
    <h1>记录自己的生活！</h1>
    <div v-if="!isLoggedIn" class="login-container">
      <component
        :is="currentComponent"
        @login="handleLogin"
        @register="handleRegister"
        @switch-component="switchComponent"
      />
    </div>
    <div v-else>
      <button @click="handleLogout">Logout</button>
      <TodoList />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import LoginForm from './components/LoginForm.vue'
import RegisterForm from './components/RegisterForm.vue'
import TodoList from './components/TodoList.vue'
import { login, register, logout } from './api'

const isLoggedIn = ref(false)
const currentComponent = ref(LoginForm)

const handleLogin = async (credentials: { username: string; password: string }) => {
  try {
    await login(credentials)
    isLoggedIn.value = true
  } catch (error) {
    console.error('Login failed:', error)
  }
}

const handleRegister = async (userData: { username: string; password: string }) => {
  try {
    await register(userData)
    console.log('Registration successful')
    currentComponent.value = LoginForm
  } catch (error) {
    console.error('Registration failed:', error)
  }
}

const handleLogout = async () => {
  try {
    await logout()
    isLoggedIn.value = false
  } catch (error) {
    console.error('Logout failed:', error)
  }
}

const switchComponent = (component: 'login' | 'register') => {
  currentComponent.value = (component === 'login' ? LoginForm : RegisterForm) as typeof LoginForm
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  width: 100vw;
  margin: 0 auto;
  padding: 20px;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

h1 {
  color: #bdc3c7;
  text-align: center;
}

button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #2980b9;
}
</style>
