<template>
  <div class="bg-zinc-900 p-6 rounded shadow-md text-white w-full max-w-md mx-auto">
    <h2 class="text-2xl mb-4">Регистрация</h2>
    <form @submit.prevent="submitForm" class="flex flex-col gap-4">
      <input
          v-model="name"
          type="text"
          placeholder="Введите имя"
          required
          class="p-2 rounded bg-zinc-800 text-white"
      />
      <button type="submit" class="bg-green-600 hover:bg-green-500 px-4 py-2 rounded">
        Зарегистрироваться
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('')

const emit = defineEmits(['registered'])

function submitForm() {
  fetch('http://localhost:5000/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: name.value })
  })
      .then(res => res.json())
      .then(data => {
        emit('registered', data) // data = { id: ..., code: ... }
      })
}
</script>