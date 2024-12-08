<template>
  <header>
    <div class="wrapper">
      <TopMenu/>
    </div>
  </header>
  <body class="flex flex-col items-center">
  <!-- Toggle button -->
  <div class="absolute top-24 right-4">
    <div @click="toggleClicked" class="bg-gray-300 w-28 h-14 flex items-center rounded-full p-1 border-gray-300 border-2 hover:cursor-pointer hover:border-core-green">
      <div :class="{'translate-x-14': isCarouselDisplay}" class="w-11 h-11 transition-all duration-500 transform bg-white rounded-full shadow-md flex items-center justify-center">
        <PhCards v-if="isCarouselDisplay" :size="32"/>
        <PhRanking v-else :size="32"/>
      </div>
    </div>
  </div>
  <!-- Carousel mode -->
  <PlayerCarousel v-if="isCarouselDisplay" :is-offense="true" class="mb-4"/>
  <div v-if="isCarouselDisplay" class="w-3/4 h-0.5 bg-gray-300 mt-8"></div>
  <PlayerCarousel v-if="isCarouselDisplay" :is-offense="false" class="mt-8 mb-16"/>
  <!-- Line ranking mode -->
  <div v-else class="flex gap-8 mt-4">
    <LineRanking :is-offense="true" name="Offensive lines"/>
    <LineRanking :is-offense="false" name="Defensive lines"/>
  </div>

  </body>
</template>

<style scoped>

</style>

<script setup>
import {ref, onMounted, onUnmounted} from 'vue';
import axios from 'axios';
import { useTeamStore } from "@/stores/team";
import TopMenu from "@/components/TopMenu.vue";
import PlayerCarousel from "@/components/PlayerCarousel.vue";
import { PhCards, PhRanking } from "@phosphor-icons/vue";
import LineRanking from "@/components/LineRanking.vue";
import { usePlayersStatsStore } from "@/stores/playersStats.js";
import { useWebSocketStore } from "@/stores/webSocket.js";

const teamStore = useTeamStore();
const playersStatsStore = usePlayersStatsStore();
const webSocketStore = useWebSocketStore();

const isCarouselDisplay = ref(false);

function toggleClicked() {
  isCarouselDisplay.value = !isCarouselDisplay.value;
}

onMounted(async () => {
  try {
    webSocketStore.connect();
    const response = await axios.get(`http://127.0.0.1:5000/players-stats?team_id=${teamStore.team.id}`);
    playersStatsStore.playersStats = response.data;
    console.log('Players stats:', playersStatsStore.playersStats);
  } catch (error) {
    console.error('Error fetching players:', error);
  }
});

</script>