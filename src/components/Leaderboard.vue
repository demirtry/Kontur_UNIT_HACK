<template>
  <div class="bg-zinc-800 p-6 rounded shadow-md text-white max-w-2xl mx-auto mt-8">
    <h2 class="text-2xl mb-4">Таблица лидеров</h2>
    <ul>
      <li
          v-for="entry in leaderboard"
          :key="entry.id"
          :class="entry.id === playerId ? 'text-green-400 font-bold' : ''"
          class="mb-2"
      >
        {{ entry.code }} — {{ entry.score }} очков
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  playerId: String
})

const leaderboard = ref([])

onMounted(() => {
  fetch('http://localhost:5000/api/leaderboard')
      .then(res => res.json())
      .then(data => {
        leaderboard.value = data // ожидается: [{id, code, score}, ...]
      })
})
</script>