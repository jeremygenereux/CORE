<template>
  <div class="flex flex-col items-center rounded-xl p-4 m-4 w-1/4 bg-gray-50 shadow-2xl min-h-[83vh] max-h-[83vh] justify-center">
    <!-- Connected players gauge -->
    <Gauge :connected-players="connectedPlayers" :total-players="totalPlayers"/>
    <div class="text-xl font-bold my-2 2xl:my-4">Connected players</div>
    <!-- Add player button -->
    <button @click="addPlayer" class="w-48 h-24 bg-gray-300 hover:bg-core-green hover:text-white my-3 2xl:my-5 flex flex-col items-center justify-center rounded-full">
      <PhUserPlus :size="40"></PhUserPlus>
      <span class="font-bold text-md mt-1">Add player</span>
    </button>
    <!-- Connect all players button -->
    <button @click="connectAllPlayers" class="w-48 h-24 bg-gray-300 hover:bg-core-green hover:text-white my-3 2xl:my-5 flex flex-col items-center justify-center rounded-full">
      <PhCellTower :size="40"/>
      <span class="font-bold text-md mt-1">Connect all players</span>
    </button>
    <!-- Disconnect all players button -->
    <button @click="disconnectAllPlayers" class="w-48 h-24 bg-gray-300 hover:bg-core-green hover:text-white my-3 2xl:my-5 flex flex-col items-center justify-center rounded-full">
      <PhPlugs :size="40"/>
      <span class="font-bold text-md mt-1">Disconnect all players</span>
    </button>
    <!-- Start Game button -->
    <button @click="startGame" class="w-48 h-24 bg-gray-300 hover:bg-core-green hover:text-white mt-3 mb-6 2xl:mt-5 2xl:mb-8 flex flex-col items-center justify-center rounded-full">
      <PhPlay :size="40" weight="bold"/>
      <span class="font-bold text-md mt-1">Start game</span>
    </button>
  </div>
</template>

<style scoped>

</style>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import {PhPlay, PhUserPlus, PhCellTower, PhPlugs} from '@phosphor-icons/vue';
import Gauge from "@/components/Gauge.vue";
import { usePlayersStore } from "@/stores/players.js";
import { useTeamStore } from "@/stores/team";
import axios from 'axios';


const router = useRouter();
const playersStore = usePlayersStore();
const teamStore = useTeamStore();

const emit = defineEmits(['open-add-player-modal']);

const connectedPlayers = computed(() => {
  return playersStore.players.filter(player => player.deviceStatus === "Connected").length;
});

const totalPlayers = computed(() => {
  return playersStore.players.length;
});

function startGame() {
  // Add any additional logic here to start the game
  router.push('/dashboard');
}

async function connectAllPlayers() {
  try {
    const response = await axios.post(`http://127.0.0.1:5000/${teamStore.team.id}/devices/connect`);
    if (response.status === 200) {
      console.log('All players connected successfully');
      // Update the players' device status in the store
      playersStore.players.forEach(player => {
        if (player.deviceId) {
          player.deviceStatus = 'Connected';
        }
      });
    } else {
      console.error('Failed to connect all players. Please try again.');
    }
  } catch (error) {
    console.error('Failed to connect all players. Please try again.', error);
  }
}

async function disconnectAllPlayers() {
  try {
    const response = await axios.post(`http://127.0.0.1:5000/${teamStore.team.id}/devices/disconnect`);
    if (response.status === 200) {
      console.log('All players disconnected successfully');
      // Update the players' device status in the store
      playersStore.players.forEach(player => {
        if (player.deviceId) {
          player.deviceStatus = 'Disconnected';
        }
      });
    } else {
      console.error('Failed to disconnect all players. Please try again.');
    }
  } catch (error) {
    console.error('Failed to disconnect all players. Please try again.', error);
  }
}

function addPlayer() {
  emit('open-add-player-modal');
}

</script>