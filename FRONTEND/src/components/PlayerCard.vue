<template>
  <div class="w-52 rounded-xl overflow-hidden border-2 hover:border-core-green shadow-lg bg-white p-2">
    <!-- Player data graph -->
    <div class="w-full h-56 rounded-xl">
      <apexchart
          type="line"
          :options="chartOptions"
          :series="chartSeries"
          width="100%"
          height="100%">
      </apexchart>
    </div>
    <div class="px-2 pt-4 pb-1">
      <p class="text-gray-700 text-base">
        {{ player.lastName }} - #{{ player.number }}
      </p>
      <div class="flex items-center font-bold text-md mt-1 mb-1">
        <PhHeartbeat :size="22" :weight="'fill'" :color="'#FF0000'" :class="{ 'beat-animation': isBeating }" class="mr-1"/>
        {{ player.hr }} BPM
      </div>
      <p class="text-gray-700 text-base">
        {{ player.state }}
      </p>
    </div>
  </div>
</template>

<style scoped>
@keyframes beat {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.5);
  }
}

.beat-animation {
  animation: beat 0.5s ease-in-out;
}
</style>

<script setup>
import { ref, computed, watch } from 'vue';
import { usePlayersStatsStore } from "@/stores/playersStats.js";
import { useHrHistoryStore } from "@/stores/hrHistory.js";
import { PhHeartbeat } from '@phosphor-icons/vue';

const playersStatsStore = usePlayersStatsStore();
const hrHistoryStore = useHrHistoryStore();

const props = defineProps({
  playerId: {
    type: Number,
    required: true
  }
});

const player = computed(() => playersStatsStore.playersStats.find(player => player.playerId === props.playerId));

const chartOptions = {
  chart: {
    type: 'line',
    toolbar: {
      show: false
    }
  },
  xaxis: {
    labels: {
      show: false
    }
  },
  stroke: {
    curve: 'smooth'
  },
  dataLabels: {
    enabled: false
  },
  tooltip: {
    enabled: false
  },
  colors: ['#FF0000']
};

const chartSeries = computed(() => [
  {
    name: 'Performance',
    data: playerData.value
  }
]);

const playerData = ref(hrHistoryStore.getHrHistory(props.playerId));
const isBeating = ref(false);

watch(() => player.value.hr, (newHr) => {
  if (newHr !== undefined) {
    playerData.value.push(newHr);
    if (playerData.value.length > 10) {
      playerData.value.shift();
    }
    isBeating.value = true;
    setTimeout(() => {
      isBeating.value = false;
    }, 500);
  }
});
</script>