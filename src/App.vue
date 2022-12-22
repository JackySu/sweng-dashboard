<script setup>
import LineChartVue from './components/LineChart.vue';
import BarChartVue from './components/BarChart.vue';
import PieChartVue from './components/PieChart.vue';
import Bar3DChartVue from './components/Bar3DChart.vue';
</script>

<template>
  <LineChartVue />
  <BarChartVue />
  <PieChartVue />
  <Bar3DChartVue />
  <button class="ui red tertiary button">Red</button>
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
