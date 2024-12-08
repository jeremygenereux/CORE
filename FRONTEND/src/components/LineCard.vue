<template>
  <div class="flex flex-col rounded-lg p-4 shadow-md xl:w-72 w-60 bg-white hover:border-core-green border-2">
    <!-- Heading section -->
    <div class="flex flex-col justify-between mb-2">
      <div class="flex items-center justify-between">
        <h2 v-if="isOffense" class="text-md text-gray-400">Offense</h2>
        <h2 v-else class="text-md text-gray-400">Defense</h2>
        <div class="relative group">
          <PhWarning v-if="hasDuplicatePositions" class="ml-2 text-red-500" :size="24" />
          <div v-if="hasDuplicatePositions" class="absolute left-0 bottom-full mb-2 hidden group-hover:block bg-black text-gray-50 text-xs rounded p-2 w-52 opacity-80">
            Warning: This line contains 2 players that play at the same position
          </div>
        </div>
      </div>
      <h2 class="text-xl font-bold">Line {{ lineNumber }}</h2>
    </div>
    <hr v-if="playersInLine.length > 0" class="border-gray-300 mb-2"/>
    <!-- Player entries section -->
    <div class="flex flex-col gap-2">
      <div v-for="player in playersInLine" :key="player.number" class="flex items-center justify-between py-2 hover:bg-gray-100">
        <div class="flex">
          <button @click="removePlayer(player)" class="hover:text-red-700">
            <PhMinusCircle :size="24" />
          </button>
          <div class="flex flex-col ml-3">
            <span>{{ player.lastName }}</span>
            <span class="text-gray-400">{{player.position}}</span>
          </div>
        </div>
        <span>#{{ player.number }}</span>
      </div>
      <!-- Add player section -->
      <template v-if="playersInLine.length < props.lineSize">
        <hr class="border-gray-300 my-2"/>
        <div class="relative mx-auto">
          <button @click="toggleDropdown" class="px-4 py-2 rounded flex items-center justify-center hover:text-green-700">
            <PhPlusCircle :size="28" />
          </button>
          <div v-if="dropdownOpen" class="absolute left-1/2 transform -translate-x-1/2 bg-white border rounded shadow-lg mt-2 w-64 z-10">
            <div v-for="player in availablePlayers" :key="player.number" @click="addPlayer(player)" class="px-4 py-2 hover:bg-gray-100 cursor-pointer">
              <div class="flex items-center justify-between">
                <span>{{ player.lastName }}</span>
                <span>#{{ player.number }}</span>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>

</style>

<script setup>
import { ref, computed } from 'vue';
import { PhMinusCircle, PhPlusCircle, PhWarning } from '@phosphor-icons/vue';
import { useLinesStore } from "@/stores/lines.js";
import axios from 'axios';

const props = defineProps({
  lineNumber: {
    type: Number,
    required: true
  },
  lineSize: {
    type: Number,
    required: true
  },
  isOffense: {
    type: Boolean,
    required: true
  },
  lineId: {
    type: Number,
    required: true
  },
});

const linesStore = useLinesStore();

const playersInLine = computed(() => {
  return linesStore.playersLines
      .filter(player => player.lineId === props.lineId)
      .sort((a, b) => positionOrder[a.position] - positionOrder[b.position]);
});
const availablePlayers = computed(() => {
  return linesStore.playersLines
      .filter(player => player.lineId === null, player => player.isOffense === props.isOffense)
      .sort((a, b) => positionOrder[a.position] - positionOrder[b.position])
});

const dropdownOpen = ref(false);

const positionOrder = {
  "Left Wing": 1,
  "Center": 2,
  "Right Wing": 3,
  "Defenseman": 4
};

const hasDuplicatePositions = computed(() => {
  if(props.isOffense){
    const positions = playersInLine.value.map(player => player.position);
    return new Set(positions).size !== positions.length;
  }
  else{
    return false;
  }
});

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value;
}

async function removePlayer(player) {
  try {
    const response = await axios.delete(`http://127.0.0.1:5000/lines/players/${player.playerId}`);
    if (response.status === 200) {
      linesStore.removePlayerFromLine(player.playerId);
      console.log('Player removed from line successfully');
    } else {
      console.error('Failed to remove player from line');
    }
  } catch (error) {
    console.error('Error removing player from line:', error);
  }
}

async function addPlayer(player) {
  try {
    const response = await axios.post(`http://127.0.0.1:5000/lines/${props.lineId}/players/${player.playerId}`);
    if (response.status === 201) {
      linesStore.addPlayerToLine(player.playerId, props.lineId);
      console.log('Player added to line successfully');
      dropdownOpen.value = false;
    } else {
      console.error('Failed to add player to line');
    }
  } catch (error) {
    console.error('Error adding player to line:', error);
  }
}
</script>