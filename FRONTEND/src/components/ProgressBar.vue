<template>
  <div class="w-full bg-gray-200 rounded-full h-4">
    <div
        class="h-4 rounded-full transition-all duration-300"
        :style="{ width: `${currentProgress}%`, backgroundColor: progressColor }"
    ></div>
  </div>
</template>

<style scoped>

</style>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  currentProgress: {
    type: Number,
    required: true
  }
});

const progressColor = computed(() => {
  const progress = props.currentProgress;
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
});
</script>