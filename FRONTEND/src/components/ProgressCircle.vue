<template>
  <div class="relative flex justify-center items-center">
    <!-- Background Circle -->
    <svg class="transform -rotate-90 w-24 h-24">
      <circle
          cx="50%"
          cy="50%"
          r="45%"
          stroke="#e5e7eb"
          stroke-width="8"
          fill="none"
      />
      <!-- Progress Circle -->
      <circle
          cx="50%"
          cy="50%"
          r="45%"
          :stroke="progressColor"
          stroke-width="8"
          stroke-dasharray="283"
          :stroke-dashoffset="circumference - (circumference * progress) / 100"
          stroke-linecap="round"
          fill="none"
          class="transition-all duration-300 ease-in-out"
      />
    </svg>
    <!-- Progress Text -->
    <div class="absolute text-xl font-semibold text-gray-700">
      {{ props.progress }}%
    </div>
  </div>
</template>

<style scoped>

</style>

<script setup>
import {computed} from "vue";

const props = defineProps({
    progress: {
      type: Number,
      required: true,
      default: 0
    }
})

const circumference = computed(() => {
  // 2πr where r = 45% of 50% (svg radius calculation)
  return 2 * Math.PI * 45;
});

const progressColor = computed(() => {
  let red = 255, green = 0;

  if (props.progress <= 25) {
    // Red to Orange
    green = Math.floor((props.progress / 25) * 128);
  } else if (props.progress <= 50) {
    // Orange to Yellow
    green = 128 + Math.floor(((props.progress - 25) / 25) * 127);
  } else if (props.progress <= 75) {
    // Yellow to Light Green
    red = 255 - Math.floor(((props.progress - 50) / 25) * 128);
    green = 255;
  } else {
    // Light Green to Darker Green
    red = 127 - Math.floor(((props.progress - 75) / 25) * 127);
    green = 200; // Darker green
  }

  return `rgb(${red}, ${green}, 75)`;
});
</script>