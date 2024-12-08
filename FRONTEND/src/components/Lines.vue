<template>
  <header>
    <div class="wrapper">
      <TopMenu/>
    </div>
  </header>
  <body>
  <div class="flex flex-col items-center my-6">
    <!-- Offensive line section -->
    <h1 class="font-bold text-2xl mt-4 mb-8">Offensive Lines</h1>
    <div class="flex items-start gap-4">
      <LineCard
          v-for="line in offensiveLines"
          :key="line.lineId"
          :line-number="line.lineNum"
          :line-size="3"
          :is-offense="true"
          :line-id="line.lineId"
      />
    </div>
    <!-- Defensive line section -->
    <h1 class="font-bold text-2xl mt-8 mb-8">Defensive Lines</h1>
    <div class="flex items-start gap-4">
      <LineCard
          v-for="line in defensiveLines"
          :key="line.lineId"
          :line-number="line.lineNum"
          :line-size="2"
          :is-offense="false"
          :line-id="line.lineId"
      />
    </div>
  </div>
  </body>
</template>

<style scoped>
</style>

<script setup>
import TopMenu from "@/components/TopMenu.vue";
import LineCard from "@/components/LineCard.vue";
import { onMounted, computed } from 'vue';
import axios from 'axios';
import { useTeamStore } from "@/stores/team";
import { useLinesStore} from "@/stores/lines.js";

const linesStore = useLinesStore();
const teamStore = useTeamStore();

const offensiveLines = computed(() => linesStore.lines.filter(line => line.isOffense));
const defensiveLines = computed(() => linesStore.lines.filter(line => !line.isOffense));

function getPlayersForLine(lineId) {
  return linesStore.playersLines.filter(playerLine => playerLine.lineId === lineId);
}

onMounted(async () => {
  try {
    const responseLines = await axios.get(`http://127.0.0.1:5000/lines?team_id=${teamStore.team.id}`);
    linesStore.lines = responseLines.data;
    const responsePlayersLines = await axios.get(`http://127.0.0.1:5000/lines/players?team_id=${teamStore.team.id}`);
    linesStore.playersLines = responsePlayersLines.data;

    console.log('Lines:', linesStore.lines);
    console.log('Players in lines:', linesStore.playersLines);
  } catch (error) {
    console.error('Error fetching lines:', error);
  }
});
</script>