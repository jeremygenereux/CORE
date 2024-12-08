<template>
  <div class="flex flex-col items-center">
  <h1 class="font-bold text-2xl mt-4 mb-4">
    {{ currentLine.name }}
  </h1>
  <div class="flex items-center justify-center">
    <button @click="prevLine" class="mr-8 p-2 hover:bg-core-green rounded-full hover:text-gray-50">
      <PhCaretDoubleLeft :size="32" />
    </button>
    <div class="flex gap-4">
      <PlayerCard
          v-for="player in currentLine.players"
          :key="player.playerId"
          :player-id="player.playerId"
          class="flex-shrink-0"
      />
    </div>
    <button @click="nextLine" class="ml-8 p-2 hover:bg-core-green rounded-full hover:text-gray-50">
      <PhCaretDoubleRight :size="32" />
    </button>
  </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import PlayerCard from './PlayerCard.vue';
import { PhCaretDoubleRight, PhCaretDoubleLeft } from '@phosphor-icons/vue';
import { usePlayersStatsStore } from "@/stores/playersStats.js";

const playersStatsStore = usePlayersStatsStore();

const props = defineProps({
  isOffense: {
    type: Boolean,
    required: true
  }
});

const currentIndex = ref(0);

const currentLine = computed(() => lines.value[currentIndex.value]);

function nextLine() {
  currentIndex.value = (currentIndex.value + 1) % lines.value.length;
}

function prevLine() {
  currentIndex.value = (currentIndex.value - 1 + lines.value.length) % lines.value.length;
}

const lines = computed(() => {
  const lines = [];
  if (props.isOffense) {
    for (let i = 1; i <= 4; i++) {
      const playersStats = playersStatsStore.playersStats.filter(player => player.lineNum === i && player.isOffense === true);
      const totalRecScore = playersStats.reduce((acc, player) => acc + player.recScore, 0);
      const avgRecScore = Math.round(totalRecScore / playersStats.length);
      lines.push({
        name: `Offensive line ${i}`,
        recScore: avgRecScore,
        players: playersStats
      });
    }
  }
  else {
    for (let i = 1; i <= 3; i++) {
      const playersStats = playersStatsStore.playersStats.filter(player => player.lineNum === i && player.isOffense === false);
      const totalRecScore = playersStats.reduce((acc, player) => acc + player.recScore, 0);
      const avgRecScore = Math.round(totalRecScore / playersStats.length);
      lines.push({
        name: `Defensive line ${i}`,
        recScore: avgRecScore,
        players: playersStats
      });
    }
  }
  return lines;
});

</script>

<style scoped>

</style>