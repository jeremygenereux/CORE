<template>
  <header>
    <div class="wrapper">
      <TopMenu/>
    </div>
  </header>
  <body>
  <div class="flex">
    <PlayersList class="m-4" @open-edit-player-modal="openEditPlayerModal"/>
    <TeamStatusSummary class="m-4" @open-add-player-modal="openNewPlayerModal"/>
  </div>

  <!-- Add Player Modal -->
  <div v-if="isNewPlayerModalOpen" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-lg w-1/3">
      <h2 class="text-xl font-bold mb-4 text-center">Create New Player</h2>
      <div class="mb-4 flex flex-col items-center">
        <label class="block text-gray-700 font-semibold">First Name</label>
        <input type="text" v-model="newPlayer.first_name" class="w-72 p-2 border border-gray-400 rounded-lg"/>
      </div>
      <div class="mb-4 flex flex-col items-center">
        <label class="block text-gray-700 font-semibold">Last Name</label>
        <input type="text" v-model="newPlayer.last_name" class="w-72 p-2 border border-gray-400 rounded-lg"/>
      </div>
      <div class="mb-4 flex flex-col items-center">
        <label class="block text-gray-700 font-semibold">Email</label>
        <input type="text" v-model="newPlayer.email" class="w-72 p-2 border border-gray-400 rounded-lg"/>
      </div>
      <div class="mb-4 flex flex-col items-center">
        <label class="block text-gray-700 font-semibold">Birth date</label>
        <input type="date" v-model="newPlayer.birth_date" class="w-72 p-2 border border-gray-400 rounded-lg"/>
      </div>
      <div v-if="errorMessage" class="mt-4 mb-1 px-4 py-2 bg-red-200 text-red-700 rounded">
        {{ errorMessage }}
      </div>
      <div class="flex justify-center gap-4">
        <button @click="closeNewPlayerModal" class="w-32 bg-gray-400 text-white py-2 rounded">Cancel</button>
        <button @click="createPlayer" class="w-32 bg-core-green text-white py-2 rounded">Create Player</button>
      </div>
    </div>
  </div>


  <!-- Edit Player Modal -->
  <div v-if="isEditPlayerModalOpen" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-lg w-1/3 h-5/6 relative">
      <h2 class="text-xl font-bold mb-4 text-center">Edit Player : {{editPlayer.firstName}} {{editPlayer.lastName}}</h2>

      <!-- Personal Information Section -->
      <div v-if="currentSection === 'personal'" class="flex flex-col items-center">
        <div class="mb-4 flex flex-row items-center gap-2">
          <div>
            <label class="ml-1 block text-gray-700 font-semibold">First Name</label>
            <input type="text" v-model="editPlayer.firstName" class="w-[8.75rem] p-2 border border-gray-400 rounded-lg"/>
          </div>
          <div>
            <label class="ml-1 block text-gray-700 font-semibold">Last Name</label>
            <input type="text" v-model="editPlayer.lastName" class="w-[8.75rem] p-2 border border-gray-400 rounded-lg"/>
          </div>
        </div>
        <div class="mb-4">
          <label class="ml-1 block text-gray-700 font-semibold">Email</label>
          <input type="text" v-model="editPlayer.email" class="w-72 p-2 border border-gray-400 rounded-lg"/>
        </div>
        <div class="mb-4">
          <label class="ml-1 block text-gray-700 font-semibold">Birth date</label>
          <input type="date" v-model="editPlayer.birthDate" class="w-72 p-2 border border-gray-400 rounded-lg"/>
        </div>
        <div class="mb-4 flex flex-row items-center gap-2">
          <div>
            <label class="ml-1 block text-gray-700 font-semibold">Num</label>
            <input type="text" v-model="editPlayer.number" class="w-14 p-2 border border-gray-400 rounded-lg"/>
          </div>
          <div>
            <label class="ml-1 block text-gray-700 font-semibold">Position</label>
            <select v-model="editPlayer.position" class="w-56 p-2 border border-gray-400 rounded-lg">
              <option value="Center">Center</option>
              <option value="Right Wing">Right Wing</option>
              <option value="Left Wing">Left Wing</option>
              <option value="Defensemen">Defensemen</option>
            </select>
          </div>
        </div>
        <!-- Button to save changes -->
        <button @click="updatePlayerInfo" class="w-24 bg-core-green text-white py-2 absolute left-1/2 bottom-20 transform -translate-x-1/2 rounded-full">Save</button>
      </div>

      <!-- Health Information Section -->
      <div v-if="currentSection === 'health'" class="flex flex-col items-center">
        <div class="mb-4">
          <label class="ml-1 block text-gray-700 font-semibold">Max HR</label>
          <input type="text" v-model="editPlayer.maxHR" class="w-72 p-2 border border-gray-400 rounded-lg"/>
        </div>
        <div>
          <label class="ml-1 block text-gray-700 font-semibold">Rest HR</label>
          <input type="text" v-model="editPlayer.restHR" class="w-72 p-2 border border-gray-400 rounded-lg"/>
        </div>
        <!-- Section to save changes and reset to default -->
        <div class="absolute left-1/2 bottom-20 transform -translate-x-1/2 flex flex-row items-center gap-2">
          <button @click="defaultPlayerHealth" class="w-36 bg-core-green text-white py-2 rounded-full">Reset to default</button>
          <button @click="updatePlayerHealth" class="w-24 bg-core-green text-white py-2 rounded-full">Save</button>
        </div>
      </div>

      <!-- Device Information Section -->
      <div v-if="currentSection === 'device'" class="flex flex-col items-center">
        <PhWatch :size="96" class="absolute top-20 left-1/2 transform -translate-x-1/2 -rotate-90" weight="thin"/>
        <PhArrowUpLeft :size="24" class="absolute top-40 left-1/2 translate-x-2 -translate-y-1 transform"/>
        <p class="w-52 text-sm text-center absolute top-44 right-10">The device ID should be located at the back of the captor</p>
        <div class="mt-56 mb-4">
          <label class="ml-1 block text-gray-700 font-semibold">Device ID</label>
          <div class="flex flex-row items-center gap-2">
            <input type="text" v-model="editPlayer.deviceId" class="w-44 p-2 border border-gray-400 rounded-lg"/>
            <span v-if="editPlayer.deviceStatus === 'Connected'" class="bg-green-500 w-2.5 h-2.5 rounded-full"></span>
            <span v-else class="bg-red-500 w-2.5 h-2.5 rounded-full"></span>
            <button @click="connectToDevice" class="w-24 bg-core-green text-white py-2 rounded-full">Connect</button>
            <button @click="disconnectFromDevice" class="w-24 bg-core-green text-white py-2 rounded-full">Disconnect</button>
          </div>
        </div>
        <!-- Button to save changes -->
        <button @click="updatePlayerDevice" class="w-24 bg-core-green text-white py-2 absolute left-1/2 bottom-20 transform -translate-x-1/2 rounded-full">Save</button>
      </div>

      <!-- Button to close modal -->
      <PhX :size="24" @click="closeEditPlayerModal" class="absolute top-4 right-4 hover:cursor-pointer"></PhX>

      <!-- Error Message Section -->
      <div v-if="errorMessage" class="w-4/5 px-4 py-2 bg-red-200 text-red-700 absolute left-1/2 bottom-32 transform -translate-x-1/2 rounded">
        {{ errorMessage }}
      </div>

      <!-- Navigation Bar -->
      <div class="flex justify-center mt-4 absolute left-1/2 bottom-2 transform -translate-x-1/2 bg-gray-300 rounded">
        <button @click="changeSection('personal')" class="mx-2 px-4 py-2 flex flex-col items-center rounded hover:cursor-pointer" :class="{'bg-core-green text-white': currentSection === 'personal'}">
          <PhUserGear :size="24"/>
          <label class="hover:cursor-pointer">Personal</label>
        </button>
        <button @click="changeSection('health')" class="mx-2 px-4 py-2 flex flex-col items-center rounded hover:cursor-pointer" :class="{'bg-core-green text-white': currentSection === 'health'}">
          <PhHeartbeat :size="24"/>
          <label class="hover:cursor-pointer">Health</label>
        </button>
        <button @click="changeSection('device')" class="mx-2 px-4 py-2 flex flex-col items-center rounded hover:cursor-pointer" :class="{'bg-core-green text-white': currentSection === 'device'}">
          <PhDevices :size="24"/>
          <label class="hover:cursor-pointer">Device</label>
        </button>
      </div>
    </div>
  </div>
  </body>
</template>

<script setup>
import TopMenu from "@/components/TopMenu.vue";
import PlayersList from "@/components/PlayersList.vue";
import TeamStatusSummary from "@/components/TeamStatusSummary.vue";
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import { useTeamStore } from "@/stores/team";
import { usePlayersStore} from "@/stores/players.js";
import { PhHeartbeat, PhDevices, PhUserGear, PhX, PhWatch, PhArrowUpLeft } from '@phosphor-icons/vue';
import {useWebSocketStore} from "@/stores/webSocket.js";

const teamStore = useTeamStore();
const playersStore = usePlayersStore();
const webSocketStore = useWebSocketStore();

const newPlayer = ref({
  first_name: null,
  last_name: null,
  birth_date: null,
  email: null
});

const editPlayer = ref(null);
const currentSection = ref('personal');

const errorMessage = ref('');

const isNewPlayerModalOpen = ref(false);
const isEditPlayerModalOpen = ref(false);

function openNewPlayerModal() {
  isNewPlayerModalOpen.value = true;
}
function closeNewPlayerModal() {
  isNewPlayerModalOpen.value = false;
  errorMessage.value = '';
  newPlayer.value = {
    first_name: null,
    last_name: null,
    birth_date: null,
    email: null
  };
}

function openEditPlayerModal(playerId) {
  isEditPlayerModalOpen.value = true;
  currentSection.value = 'personal';
  // Fetch player data by ID and populate the form
  const player = playersStore.players.find(player => player.id === playerId);
  if (player) {
    editPlayer.value = {...player};
    console.log('Opening edit player modal for player:', editPlayer.value);
  }
}
function closeEditPlayerModal() {
  isEditPlayerModalOpen.value = false;
  errorMessage.value = '';
  editPlayer.value = null;
}

function changeSection(section) {
  currentSection.value = section;
  errorMessage.value = '';
}

async function createPlayer() {
  console.log('Creating player:', newPlayer.value);
  // Validate fields
  if (!newPlayer.value.first_name || !newPlayer.value.birth_date || !newPlayer.value.last_name) {
    console.warn('First name, last name and birth date are required. Please fill in the missing information.');
    errorMessage.value = 'First name, last name and birth date are required. Please fill in the missing information.';
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:5000/players', {
      team_id: teamStore.team.id,
      first_name: newPlayer.value.first_name,
      last_name: newPlayer.value.last_name,
      birth_date: newPlayer.value.birth_date,
      email: newPlayer.value.email
    });

    if (response.status === 201) {
      console.log('Player created:', response.data);
      const newPlayer = {
        id: response.data.id,
        firstName: response.data.first_name,
        lastName: response.data.last_name,
        birthDate: response.data.birth_date,
        email: response.data.email,
        number: response.data.number,
        position: response.data.position,
        deviceStatus: undefined,
        deviceId: undefined,
        maxHR: undefined,
        restHR: undefined
      }
      playersStore.addPlayer(newPlayer);
      closeNewPlayerModal();
    } else {
      errorMessage.value = 'Failed to create player. Please try again.';
    }
  } catch (error) {
    errorMessage.value = 'Failed to create player. Please try again.';
  }
}

async function updatePlayerInfo() {
  // Validate fields
  if (!editPlayer.value.firstName || !editPlayer.value.birthDate || !editPlayer.value.lastName) {
    console.warn('First name, last name and birth date are required. Please fill in the missing information.');
    errorMessage.value = 'First name, last name and birth date are required. Please fill in the missing information.';
    return;
  }

  try {
    const response = await axios.put(`http://127.0.0.1:5000/players/${editPlayer.value.id}`, {
      first_name: editPlayer.value.firstName,
      last_name: editPlayer.value.lastName,
      birth_date: editPlayer.value.birthDate,
      email: editPlayer.value.email,
      number: editPlayer.value.number,
      position: editPlayer.value.position
    });

    if (response.status === 200) {
      playersStore.updatePlayer(editPlayer.value.id, editPlayer.value);
      closeEditPlayerModal();
    } else {
      errorMessage.value = 'Failed to update player. Please try again.';
    }
  } catch (error) {
    errorMessage.value = 'Failed to update player. Please try again.';
  }
}

async function updatePlayerHealth() {
  console.log(`Player ${editPlayer.value.id} has new resting HR: ${editPlayer.value.restHR} and max HR: ${editPlayer.value.maxHR}`);
  // Validate fields
  if (!editPlayer.value.maxHR || !editPlayer.value.restHR) {
    console.warn('Maximum and rest hearth rates are required. Please fill in the missing information.');
    errorMessage.value = 'Maximum and rest hearth rates are required. Please fill in the missing information.';
    return;
  }

  try {
    const response = await axios.post(`http://127.0.0.1:5000/players/${editPlayer.value.id}/health`, {
      max_HR: editPlayer.value.maxHR,
      rest_HR: editPlayer.value.restHR
    });

    if (response.status === 200) {
      playersStore.updatePlayer(editPlayer.value.id, editPlayer.value);
      closeEditPlayerModal();
    } else {
      errorMessage.value = 'Failed to update player. Please try again.';
    }
  } catch (error) {
    errorMessage.value = 'Failed to update player. Please try again.';
  }
}

async function defaultPlayerHealth() {
  console.log(`Setting default rest and max HR for Player ${editPlayer.value.id}`);
  try {
    const response = await axios.post(`http://127.0.0.1:5000/players/${editPlayer.value.id}/health/default`);

    if (response.status === 200) {
      editPlayer.value.restHR = response.data.rest_HR;
      editPlayer.value.maxHR = response.data.max_HR;
      console.log('Player health reset to default:', editPlayer.value);
      playersStore.updatePlayer(editPlayer.value.id, editPlayer.value);
      closeEditPlayerModal();
    } else {
      errorMessage.value = 'Failed to update player. Please try again.';
    }
  } catch (error) {
    errorMessage.value = 'Failed to update player. Please try again.';
  }
}

async function updatePlayerDevice() {
  console.log(`Player ${editPlayer.value.id} has new device: ${editPlayer.value.deviceId}`);
  // Validate fields
  if (!editPlayer.value.deviceId) {
    console.warn('DeviceId is required. Please fill in the missing information.');
    errorMessage.value = 'Device ID is required. Please fill in the missing information.';
    return;
  }

  try {
    const response = await axios.post(`http://127.0.0.1:5000/devices`, {
      player_id: editPlayer.value.id,
      device_id: editPlayer.value.deviceId
    });

    if (response.status === 200) {
      playersStore.updatePlayer(editPlayer.value.id, editPlayer.value);
      closeEditPlayerModal();
    } else {
      errorMessage.value = 'Failed to update player device. Please try again.';
    }
  } catch (error) {
    errorMessage.value = 'Failed to update player device. Please try again.';
  }
}

async function connectToDevice() {
  console.log(`Connecting to device ${editPlayer.value.deviceId}`);
  try {
    const response = await axios.post(`http://127.0.0.1:5000/${teamStore.team.id}/devices/${editPlayer.value.deviceId}/connect`);

    if (response.status === 200) {
      console.log('Device connected successfully');
      playersStore.players.find(player => player.id === editPlayer.value.id).deviceStatus = 'Connected';
      if(editPlayer){
        editPlayer.value.deviceStatus = 'Connected';
      }
    } else {
      errorMessage.value = 'Failed to connect to device. Please try again.';
    }
  } catch (error) {
    errorMessage.value = 'Failed to connect to device. Please try again.';
  }
}

async function disconnectFromDevice() {
  console.log(`Disconnecting from device ${editPlayer.value.deviceId}`);
  try {
    const response = await axios.post(`http://127.0.0.1:5000/${teamStore.team.id}/devices/${editPlayer.value.deviceId}/disconnect`);

    if (response.status === 200) {
      console.log('Device disconnected successfully');
      playersStore.players.find(player => player.id === editPlayer.value.id).deviceStatus = 'Disconnected';
      if(editPlayer){
        editPlayer.value.deviceStatus = 'Disconnected';
      }
    } else {
      errorMessage.value = 'Failed to disconnect to device. Please try again.';
    }
  } catch (error) {
    errorMessage.value = 'Failed to disconnect to device. Please try again.';
  }
}

onMounted(async () => {
  try {
    webSocketStore.connect();
    const response = await axios.get(`http://127.0.0.1:5000/players?team_id=${teamStore.team.id}`);
    playersStore.players = response.data;
  } catch (error) {
    console.error('Error fetching players:', error);
  }
});
</script>

<style scoped>
</style>