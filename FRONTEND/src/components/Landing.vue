<template>
  <div class="flex items-center justify-center bg-white min-h-screen">
    <div class="flex w-full max-w-4xl p-8">
      <!-- Connection Section -->
      <div class="flex flex-col justify-center w-1/2">
        <!-- Input Section -->
        <div class="flex flex-col justify-center bg-gray-200 rounded-3xl py-4 px-8">
          <label class="mb-2 ml-4 text-gray-700 font-semibold">Email</label>
          <input v-model="email" type="email" class="mb-4 p-2 border border-gray-300 rounded-full" />
          <label class="mb-2 ml-4 text-gray-700 font-semibold">Password</label>
          <input v-model="password" type="password" class="p-2 border border-gray-300 rounded-full" />
        </div>
        <!-- Button Section -->
        <button @click="handleLogin" class="mt-4 mb-1 px-4 py-2 bg-gray-200 text-gray-700 font-bold rounded-full hover:bg-core-green hover:text-gray-50 w-full">Log in</button>
        <div class="text-center text-gray-700">
          Don’t have an account?
          <router-link to="/signup" class="text-blue-500 font-semibold hover:underline">Sign up for free</router-link>
        </div>
      </div>
      <!-- Divider -->
      <div class="border-l border-gray-300 mx-8"></div>
      <!-- Logo Section -->
      <div class="flex items-center justify-center w-1/2">
        <img alt="Logo" class="w-128 h-128" src="../assets/LogoCouleur.svg" />
      </div>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useWebSocketStore } from '@/stores/webSocket';
import { useTeamStore } from '@/stores/team';
import { usePlayersStore } from '@/stores/players';
import { usePlayersStatsStore } from '@/stores/playersStats';
import { useLinesStore } from '@/stores/lines';
import { useHrHistoryStore } from '@/stores/hrHistory';

const email = ref('');
const password = ref('');
const authStore = useAuthStore();
const router = useRouter();
const webSocketStore = useWebSocketStore();
const teamStore = useTeamStore();
const playersStore = usePlayersStore();
const playersStatsStore = usePlayersStatsStore();
const linesStore = useLinesStore();
const hrHistoryStore = useHrHistoryStore();


const handleLogin = async () => {
  try {
    await authStore.login(email.value, password.value);
    router.push('/teamSelect');
  } catch (error) {
    alert('Login failed. Please check your credentials.');
  }
};

onMounted(() => {
  // Clear all stores and disconnect websocket on landing page
  teamStore.clearTeam();
  authStore.logout();
  playersStore.clearPlayers();
  playersStatsStore.clearPlayersStats();
  linesStore.clearAll();
  hrHistoryStore.clearHrHistory();
  webSocketStore.disconnect();
});

</script>