<template>
  <div class="flex flex-col items-center">
    <h1 class="font-bold text-2xl mb-4">{{ props.name }}</h1>
    <transition-group name="list" tag="div" class="w-full">
      <div v-for="line in sortedLines" :key="line.name" class="w-full mb-4">
        <line-score-card :line="line"/>
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.list-move {
  transition: transform 0.5s ease;
}
.list-enter-active, .list-leave-active {
  transition: all 0.3s ease;
}
.list-enter-from, .list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>

<script setup>
import { computed } from 'vue';
import LineScoreCard from "@/components/LineScoreCard.vue";
import { usePlayersStatsStore } from "@/stores/playersStats.js";

const playersStatsStore = usePlayersStatsStore();

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  isOffense: {
    type: Boolean,
    required: true
  }
});

const unsortedLines = computed(() => {
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


const sortedLines = computed(() => {
  return unsortedLines.value.slice().sort((a, b) => b.recScore - a.recScore);
});
</script>