<template>
  <div class="min-h-screen bg-black text-green-400 font-mono p-4 flex flex-col items-center justify-center">

    <!-- Игра + таблица лидеров после регистрации -->
    <div v-if="step === 'game'" class="w-full max-w-3xl">
      <GameBoard :player="player" @gameFinished="onGameFinish" />
      <Leaderboard :playerId="player.id" />
    </div>

    <!-- Плашка регистрации внизу -->
    <div
        class="fixed bottom-0 left-0 right-0 bg-zinc-900 p-4 text-white flex justify-center items-center"
    >
      <template v-if="step === 'register'">
        <form @submit.prevent="submitRegistration" class="flex gap-2 w-full max-w-md">
          <input
              v-model="name"
              type="text"
              placeholder="Введите имя"
              required
              class="flex-grow p-2 rounded bg-zinc-800 text-white"
          />
          <button
              type="submit"
              class="bg-green-600 hover:bg-green-500 px-4 py-2 rounded"
          >
            Зарегистрироваться
          </button>
        </form>
      </template>

      <template v-else-if="step === 'registered'">
        <div class="flex flex-col items-center gap-2">
          <div>✅ Регистрация успешна!</div>
          <div>ID: <code>{{ player.id }}</code></div>
          <div>Код: <code>{{ player.code }}</code></div>
          <button
              @click="startGame"
              class="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded mt-2"
          >
            Начать игру
          </button>
        </div>
      </template>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import GameBoard from './components/GameBoard.vue'
import Leaderboard from './components/Leaderboard.vue'

const step = ref('register') // register | registered | game
const name = ref('')
const player = ref({ id: '', code: '' })

function submitRegistration() {
  fetch('http://localhost:5000/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: name.value })
  })
      .then(res => res.json())
      .then(data => {
        player.value = { id: data.id, code: data.code }
        step.value = 'registered'
      })
      .catch(() => {
        alert('Ошибка регистрации, попробуйте снова')
      })
}

function startGame() {
  step.value = 'game'
}

function onGameFinish(score) {
  fetch('http://localhost:5000/api/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: player.value.id, score })
  })
      .then(res => res.json())
      .then(data => {
        console.log('Результат сохранен:', data)
      })
}
</script>

<style>
/* Если нужно, добавь свои стили */
</style>
