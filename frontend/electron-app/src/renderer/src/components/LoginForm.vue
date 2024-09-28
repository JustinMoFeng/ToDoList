<template>
  <div class="login-form">
    <h2>登录</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">用户名:</label>
        <input v-model="username" type="text" id="username" required />
      </div>
      <div class="form-group">
        <label for="password">密码:</label>
        <input v-model="password" type="password" id="password" required />
      </div>
      <button type="submit">登录</button>
    </form>
    <p>没有账号? <a href="#" @click.prevent="switchToRegister">点击这里注册</a></p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const username = ref('')
const password = ref('')

const emit = defineEmits(['login', 'switch-component'])

const handleSubmit = () => {
  emit('login', { username: username.value, password: password.value })
}

const switchToRegister = () => {
  emit('switch-component', 'register')
}
</script>

<style scoped>
.login-form {
  width: 50%;
  border: 1px solid purple;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #bdc3c7;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #bdc3c7;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 16px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #2980b9;
}

p {
  margin-top: 15px;
  text-align: center;
}

a {
  color: #3498db;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
