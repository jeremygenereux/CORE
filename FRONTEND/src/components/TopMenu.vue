<template>
  <!-- Navigation bar -->
  <nav class="flex justify-between items-center px-4 py-1 bg-white border-b border-gray-300">
    <!-- Logo -->
    <img alt="Logo CORE" class="w-16 h-16" src="../assets/LogoCouleur.svg" />
    <div class="flex-1"></div>
    <!-- Team name (centered) -->
    <div v-if="teamStore.team?.team_name != null" class="absolute left-1/2 transform -translate-x-1/2">
      <h1 class="text-xl font-bold">{{ teamStore.team?.team_name }}</h1>
    </div>
    <div class="flex gap-4 items-center">
      <!-- Button to dashboard -->
      <router-link v-if="teamStore.team?.team_name != null" :to="`/dashboard`">
        <button class="px-2 lg:px-4 py-2 bg-transparent text-black rounded hover:bg-core-green hover:text-gray-50">Dashboard</button>
      </router-link>
      <div v-if="teamStore.team?.team_name != null" class="border-l border-gray-300 h-10"></div>
      <!-- Button to team -->
      <router-link v-if="teamStore.team?.team_name != null" :to="`/team`">
        <button class="px-2 lg:px-4 py-2 bg-transparent text-black rounded hover:bg-core-green hover:text-gray-50">Team</button>
      </router-link>
      <div v-if="teamStore.team?.team_name != null" class="border-l border-gray-300 h-10"></div>
      <!-- Button to Lines -->
      <router-link v-if="teamStore.team?.team_name != null" :to="`/lines`">
        <button class="px-2 lg:px-4 py-2 bg-transparent text-black rounded hover:bg-core-green hover:text-gray-50">Lines</button>
      </router-link>
      <!-- User icon with dropdown -->
      <div class="relative">
        <PhUserCircle :size="42" @click="toggleDropdown" class="cursor-pointer"/>
        <div v-if="dropdownVisible" class="absolute right-0 z-10 mt-2 w-48 bg-white border border-gray-300 rounded shadow-lg">
          <ul>
            <li class="px-4 py-2 hover:bg-gray-100 cursor-pointer" @click="logOut">Log out</li>
            <li class="px-4 py-2 hover:bg-gray-100 cursor-pointer" @click="changeTeam">Change team</li>
            <li class="px-4 py-2 hover:bg-gray-100 cursor-pointer">User settings</li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { PhUserCircle } from '@phosphor-icons/vue';
import { useTeamStore } from "@/stores/team";
import { useAuthStore } from "@/stores/auth";
import { usePlayersStore } from "@/stores/players";
import { useWebSocketStore } from "@/stores/webSocket";
import { usePlayersStatsStore } from "@/stores/playersStats";
import { useLinesStore} from "@/stores/lines.js";
import { useHrHistoryStore } from "@/stores/hrHistory.js";

const teamStore = useTeamStore();
const authStore = useAuthStore();
const playersStore = usePlayersStore();
const webSocketStore = useWebSocketStore();
const playersStatsStore = usePlayersStatsStore();
const linesStore = useLinesStore();
const hrHistoryStore = useHrHistoryStore();
const dropdownVisible = ref(false);
const router = useRouter();

function toggleDropdown() {
  dropdownVisible.value = !dropdownVisible.value;
}
function logOut() {
  teamStore.clearTeam();
  authStore.logout();
  playersStore.clearPlayers();
  webSocketStore.disconnect();
  playersStatsStore.clearPlayersStats();
  linesStore.clearAll();
  hrHistoryStore.clearHrHistory();
  router.push('/');
}

function changeTeam() {
  playersStatsStore.clearPlayersStats();
  teamStore.clearTeam();
  playersStore.clearPlayers()
  linesStore.clearAll();
  hrHistoryStore.clearHrHistory();
  router.push('/teamSelect');
}

</script>

<style scoped>
</style>