<template>
  <header>
    <div class="wrapper">
      <TopMenu/>
    </div>
  </header>
  <body>
  <h1 class="text-center text-3xl font-bold mt-16 mb-8">Select a team</h1>
  <div class="flex flex-wrap justify-center gap-4 p-4">
    <div
        v-for="team in teams"
        :key="team.team_name"
        class="w-64 h-64 border-4 hover:border-core-green rounded-lg shadow-lg p-4 cursor-pointer bg-gray-200 flex flex-col items-center"
        @click="goToDashboard(team)"
    >
      <h2 class="text-black text-xl font-bold my-2">{{ team.team_name }}</h2>
      <div class="w-24 h-24 rounded-lg p-2 mt-6 flex items-center justify-center" :style="{ backgroundColor: team.primary_color }">
        <PhTShirt :size="96" :color="team.secondary_color" weight="bold"/>
      </div>
    </div>
    <div class="w-64 h-64 border-4 hover:border-core-green rounded-lg shadow-lg p-4 cursor-pointer bg-gray-200 flex flex-col items-center" @click="openModal">
      <h2 class="text-black text-xl font-bold my-2">Create new team</h2>
      <div class="w-24 h-24 rounded-lg p-2 mt-6 flex items-center justify-center bg-gray-400">
        <PhPlus :size="60" weight="regular"/>
      </div>
    </div>
  </div>

  <!-- Modal -->
  <div v-if="isModalOpen" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-lg w-1/3">
      <h2 class="text-xl font-bold mb-4 text-center">Create New Team</h2>
      <div class="mb-4 flex flex-col items-center">
        <label class="block text-gray-700 font-semibold">Team Name</label>
        <input type="text" v-model="newTeam.team_name" class="w-72 p-2 border rounded"/>
      </div>
      <div class="mb-4 flex flex-col items-center">
        <label class="block text-gray-700 font-semibold">Primary Color</label>
        <input type="color" v-model="newTeam.primary_color" class="ml-2 w-10 h-10"/>
      </div>
      <div class="mb-4 flex flex-col items-center">
        <label class="block text-gray-700 font-semibold">Secondary Color</label>
        <input type="color" v-model="newTeam.secondary_color" class="ml-2 w-10 h-10"/>
      </div>
      <!-- Validation Message Section -->
      <div v-if="errorMessage" class="mt-4 mb-1 px-4 py-2 bg-red-200 text-red-700 rounded">
        {{ errorMessage }}
      </div>
      <div class="flex justify-center gap-4">
        <button @click="closeModal" class="w-32 bg-gray-400 text-white py-2 rounded">Cancel</button>
        <button @click="createTeam" class="w-32 bg-core-green text-white py-2 rounded">Create Team</button>
      </div>
    </div>
  </div>
  </body>
</template>

<style scoped>
</style>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { PhTShirt, PhPlus } from '@phosphor-icons/vue';
import TopMenu from "@/components/TopMenu.vue";
import { useTeamStore } from "@/stores/team";
import { useAuthStore } from "@/stores/auth";

const teamStore = useTeamStore();
const authStore = useAuthStore();

const teams = ref([]);

const isModalOpen = ref(false);
const newTeam = ref({
  team_name: '',
  primary_color: '#000000',
  secondary_color: '#FFFFFF'
});
const errorMessage = ref('');

const router = useRouter();

const goToDashboard = (team) => {
  teamStore.chooseTeam(team);
  router.push(`/team`);
};

function openModal() {
  isModalOpen.value = true;
}
function closeModal() {
  isModalOpen.value = false;
  errorMessage.value = '';
}

async function createTeam() {
  // Validate fields
  if (!newTeam.value.team_name || !newTeam.value.primary_color || !newTeam.value.secondary_color) {
    errorMessage.value = 'All fields are required. Please fill in the missing information.';
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:5000/teams', {
      coach_id: authStore.coach.coachId,
      team_name: newTeam.value.team_name,
      primary_color: newTeam.value.primary_color,
      secondary_color: newTeam.value.secondary_color
    });

    if (response.status === 201) {
      teams.value.push(response.data);
      errorMessage.value = '';
      closeModal();
    } else {
      errorMessage.value = 'Failed to create team. Please try again.';
    }
  } catch (error) {
    errorMessage.value = 'Failed to create team. Please try again.';
  }
}

onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/teams?coach_id=${authStore.coach.coachId}`);
    teams.value = response.data;
  } catch (error) {
    console.error('Error fetching teams:', error);
  }
});
</script>