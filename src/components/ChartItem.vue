
<script setup>
  import LineChartVue from './LineChart.vue';
  import BarChartVue from './BarChart.vue';
  import PieChartVue from './PieChart.vue';
  import Bar3DChartVue from './Bar3DChart.vue';
</script>

<template>
  <div class="container">
    <button
      class="ui red tertiary button"
      @click="graphNumber=0"
    >
      Line Chart
    </button>
    <button
      class="ui orange tertiary button"
      @click="graphNumber=1"
    >
      Bar Chart
    </button>
    <button
      class="ui yellow tertiary button"
      @click="graphNumber=2"
    >
      Pie Chart
    </button>
    <button
      class="ui olive tertiary button"
      @click="graphNumber=3"
    >
      3D Chart
    </button>
    <br/>
    <div>
      <LineChartVue v-if="graphNumber == 0"></LineChartVue>
      <BarChartVue v-if="graphNumber == 1"></BarChartVue>
      <PieChartVue v-if="graphNumber == 2"></PieChartVue>
      <Bar3DChartVue v-if="graphNumber == 3"></Bar3DChartVue>
    </div>
  </div>
</template>

<script scoped>
  export default {
    data() {
      return {
        graphNumber: 0,
      }
    }
  }
</script>
