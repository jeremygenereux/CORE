<template>
  <!-- All players -->
  <div class="flex flex-col bg-gray-50 rounded-xl p-4 w-2/3 h-3/4 min-h-[83vh] max-h-[83vh] shadow-2xl">
    <!-- Title, Search Bar, and Sort By Dropdown -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">All Players</h2>
      <div class="relative">
        <input ref="searchInput" type="text" placeholder="Search" class="p-2 pl-10 rounded-full bg-gray-200" v-model="searchQuery"/>
        <PhMagnifyingGlass class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 cursor-text" @click="focusSearchInput"/>
      </div>
      <select class="p-2 bg-gray-200 rounded-full" v-model="sortKey">
        <option v-for="option in sortOptions" :key="option.value" :value="option.value" :class="{'font-bold': sortKey === option.value}">
          Sort by {{ option.text }}
        </option>
      </select>
    </div>
    <!-- Player Table -->
    <div class="overflow-y-auto scrollbar-track-amber-400 max-h-[75vh]">
      <table class="min-w-full bg-white text-left">
        <thead>
        <tr>
          <th class="py-4 px-4 border-b font-semibold text-gray-400">Name</th>
          <th class="py-4 px-4 border-b font-semibold text-gray-400">Number</th>
          <th class="py-4 px-4 border-b font-semibold text-gray-400">Position</th>
          <th class="py-4 px-4 border-b lg:table-cell hidden font-semibold text-gray-400">Line</th>
          <th class="py-4 px-4 border-b font-semibold text-gray-400">Device&nbspID</th>
          <th class="py-4 px-4 border-b font-semibold text-gray-400">Device&nbspStatus</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="player in filteredPlayers" :key="player.deviceId" class="hover:bg-gray-100 border-b p-4" @click="editPlayer(player.id)">
          <td class="py-5 px-4 ">{{ player.firstName }} {{ player.lastName }}</td>
          <td class="py-5 px-4 ">{{ player.number }}</td>
          <td class="py-5 px-4 ">{{ player.position }}</td>
          <td class="py-5 px-4 lg:table-cell hidden">{{ getLineInfo(player) }}</td>
          <td class="py-5 px-4 ">{{ player.deviceId }}</td>
          <td class="py-5 px-4 " >
            <div class="text-center bg-opacity-25 border-[1px] rounded-md w-28" :class="{'bg-green-500 border-green-600 text-green-700': player.deviceStatus === 'Connected', 'bg-red-500 border-red-600 text-red-500': player.deviceStatus === 'Disconnected'}">
              {{ player.deviceStatus }}
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import {ref, computed} from 'vue';
import {PhMagnifyingGlass} from '@phosphor-icons/vue';
import {usePlayersStore} from "@/stores/players.js";

const playersStore = usePlayersStore();

const emit = defineEmits(['open-edit-player-modal']);

const sortKey = ref('firstName');
const searchQuery = ref('');
const searchInput = ref(null);

const sortOptions = [
  {value: 'firstName', text: 'Name'},
  {value: 'number', text: 'Number'},
  {value: 'position', text: 'Position'},
  {value: 'deviceStatus', text: 'Device Status'}
];

const filteredPlayers = computed(() => {
  const query = searchQuery.value;
  return [...playersStore.players]
      .filter(player =>
          Object.values(player).some(value =>
              String(value).toLowerCase().includes(query)
          )
      )
      .sort((a, b) => {
        if (a[sortKey.value] < b[sortKey.value]) return -1;
        if (a[sortKey.value] > b[sortKey.value]) return 1;
        return 0;
      });
});

const getLineInfo = (player) => {
  if (player.isOffense === true)
    return `Offensive line ${player.lineNum}`
  else if (player.isOffense === false)
    return `Defensive line ${player.lineNum}`;
  else
    return ''
};

function focusSearchInput() {
  searchInput.value.focus();
}

function editPlayer(playerId) {
  emit('open-edit-player-modal', playerId);
}
</script>