
<script setup>
  import ChartLoaderVue from './ChartLoader.vue';
</script>

<template>
  <div class="chart_container">
    <button
      class="ui red tertiary button"
      @click="graphNumber=0"
    >
      Bar Chart
    </button>
    <button
      class="ui orange tertiary button"
      @click="graphNumber=1"
    >
      Pie Chart
    </button>
    <button
      class="ui yellow tertiary button"
      @click="graphNumber=2"
    >
      3D Chart
    </button>
    <button
      class="ui olive tertiary button"
      @click="graphNumber=3"
    >
      Line Chart
    </button>
    <br/>
    <div>
      <ChartLoaderVue :selectChart="'BarChartVue'" v-if="graphNumber == 0" />
      <ChartLoaderVue :selectChart="'PieChartVue'" v-if="graphNumber == 1" />
      <ChartLoaderVue :selectChart="'Bar3DChartVue'" v-if="graphNumber == 2" />
      <ChartLoaderVue :selectChart="'LineChartVue'" v-if="graphNumber == 3" />
    </div>
  </div>
</template>

<script scoped>
  export default {
    data() {
      return {
        graphNumber: 0,
      }
    },
    components: {
      ChartLoaderVue
    }
  }
</script>
