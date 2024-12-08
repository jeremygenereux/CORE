<script setup>
import { computed } from 'vue';

const props = defineProps({
  connectedPlayers: {
    type: Number,
    required: true
  },
  totalPlayers: {
    type: Number,
    required: true
  }
})

const percentage = computed(() => {
  if (props.totalPlayers === 0) return 0;
  return Math.round((props.connectedPlayers / props.totalPlayers) * 100);
});


const cssTransformRotateValue = computed(() => {
  const percentageAsFraction = percentage.value / 100
  const halfPercentage = percentageAsFraction / 2

  return `${halfPercentage}turn`
})

</script>

<template>
  <div class="w-full 2xl:max-w-[250px] max-w-[200px]">
    <div class="relative w-full h-0 pb-[50%] bg-gray-300 overflow-hidden rounded-t-[100%_200%]">
      <div class="absolute top-full left-0 w-full h-full bg-core-green origin-top transition-transform duration-200 ease-out" :style="{ transform: `rotate(${cssTransformRotateValue})` }"></div>
      <div class="absolute top-[25%] left-1/2 w-[75%] h-[150%] bg-gray-50 transform -translate-x-1/2 rounded-full flex items-center justify-center pb-[25%] box-border font-bold text-4xl">
        {{ percentage }}%
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
