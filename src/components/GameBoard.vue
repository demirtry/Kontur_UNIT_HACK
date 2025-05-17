<template>
  <div class="bg-zinc-800 p-6 rounded shadow-md text-white max-w-2xl mx-auto mt-8">
    <h2 class="text-2xl mb-4">Игра началась!</h2>
    <p class="mb-4">Игрок: {{ player.code }}</p>

    <div v-if="!gameOver">
      <p class="mb-4">Текущий счёт: {{ score }}</p>
      <button @click="addScore" class="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded">
        +10 очков
      </button>
      <button @click="finishGame" class="bg-red-600 hover:bg-red-500 px-4 py-2 rounded ml-4">
        Завершить игру
      </button>
    </div>

    <div v-else>
      <p class="text-lg font-bold text-green-400">Игра завершена! Итоговый счёт: {{ score }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  player: Object
})

const emit = defineEmits(['gameFinished'])

const score = ref(0)
const gameOver = ref(false)

function addScore() {
  score.value += 10
}

function finishGame() {
  gameOver.value = true
  emit('gameFinished', score.value)
}
</script>