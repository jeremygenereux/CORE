<template>
  <div class="rounded-xl overflow-hidden border-2 hover:border-core-green shadow-lg bg-white p-2 w-96 flex-col justify-center">
    <h2 class="font-semibold text-xl mb-2 text-center">{{ props.line.name }}</h2>
    <div class="flex justify-center gap-8 mb-2">
      <ul class="flex flex-col justify-center">
        <li v-for="player in props.line.players" :key="player.number" class="flex py-2 items-center border-b last:border-b-0">
          <!-- Player progress element -->
          <div
              class="rounded-xl w-10 h-10 mx-1 font-bold text-center flex items-center justify-center border-2 border-black transition-all duration-300 ease-in-out"
              :style="{ backgroundColor: getProgressColor(player.recScore) }"
          >
            {{ player.recScore }}
          </div>
          <span class="ml-1">{{ player.lastName }}</span>
          <span class="font-semibold ml-1 w-8">#{{ player.number }}</span>
        </li>
      </ul>
      <!-- Line progress circle -->
      <progress-circle :progress="props.line.recScore"></progress-circle>
    </div>
  </div>
</template>

<style scoped>

</style>

<script setup>
import ProgressCircle from "@/components/ProgressCircle.vue";
import ProgressBar from "@/components/ProgressBar.vue";


const props = defineProps({
  line: {
    type: Object,
    required: true
  }
});

function getProgressColor(progress) {
  let red = 255, green = 0;

  if (progress <= 25) {
    // Red to Orange
    green = Math.floor((progress / 25) * 128);
  } else if (progress <= 50) {
    // Orange to Yellow
    green = 128 + Math.floor(((progress - 25) / 25) * 127);
  } else if (progress <= 75) {
    // Yellow to Light Green
    red = 255 - Math.floor(((progress - 50) / 25) * 128);
    green = 255;
  } else {
    // Light Green to Darker Green
    red = 127 - Math.floor(((progress - 75) / 25) * 127);
    green = 200; // Darker green
  }

  return `rgb(${red}, ${green}, 75)`;
}

</script>