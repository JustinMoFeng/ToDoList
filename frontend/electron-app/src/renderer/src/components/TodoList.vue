<template>
  <div class="todo-list">
    <h2>Todo List</h2>
    <form @submit.prevent="addTodo">
      <input v-model="newTodoTitle" type="text" placeholder="New todo" required />
      <input v-model="newTodoDescription" type="text" placeholder="Description" />
      <select v-model="newTodoPriority">
        <option value="1">Low</option>
        <option value="2">Medium</option>
        <option value="3">High</option>
      </select>
      <button type="submit">Add Todo</button>
    </form>
    <ul>
      <li v-for="todo in todos" :key="todo.id">
        <input v-model="todo.status" type="checkbox" @change="updateTodo(todo)" />
        <span :class="{ completed: todo.status }">{{ todo.title }}</span>
        <p>{{ todo.description }}</p>
        <select v-model="todo.priority" @change="updateTodo(todo)">
          <option value="1">Low</option>
          <option value="2">Medium</option>
          <option value="3">High</option>
        </select>
        <button @click="deleteTodo(todo.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  getTodos,
  addTodo as apiAddTodo,
  updateTodo as apiUpdateTodo,
  deleteTodo as apiDeleteTodo
} from '../api'

interface Todo {
  id: number
  title: string
  description: string
  status: boolean
  priority: number
}

const todos = ref<Todo[]>([])
const newTodoTitle = ref('')
const newTodoDescription = ref('')
const newTodoPriority = ref(1)

onMounted(async () => {
  try {
    todos.value = await getTodos()
  } catch (error) {
    console.error('Failed to fetch todos:', error)
  }
})

const addTodo = async () => {
  try {
    const newTodo = await apiAddTodo({
      title: newTodoTitle.value,
      description: newTodoDescription.value,
      priority: newTodoPriority.value
    })
    todos.value.push(newTodo)
    newTodoTitle.value = ''
    newTodoDescription.value = ''
    newTodoPriority.value = 1
  } catch (error) {
    console.error('Failed to add todo:', error)
  }
}

const updateTodo = async (todo: Todo) => {
  try {
    await apiUpdateTodo(todo.id, todo)
  } catch (error) {
    console.error('Failed to update todo:', error)
  }
}

const deleteTodo = async (id: number) => {
  try {
    await apiDeleteTodo(id)
    todos.value = todos.value.filter((todo) => todo.id !== id)
  } catch (error) {
    console.error('Failed to delete todo:', error)
  }
}
</script>

<style scoped>
.completed {
  text-decoration: line-through;
}
</style>
