<script setup>
  import SelectRepoVue from './components/SelectRepo.vue';
  import ChartItemVue from './components/ChartItem.vue';
</script>

<template>
  <ChartItemVue />
  <SelectRepoVue />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
