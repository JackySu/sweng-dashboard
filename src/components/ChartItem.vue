
<script setup>
  import ChartLoaderVue from './ChartLoader.vue';
</script>

<template>
  <div class="chart_container">
    <button
      class="ui red tertiary button"
      @click="setSelection(0)"
    >
      Bar Chart
    </button>
    <button
      class="ui orange tertiary button"
      @click="setSelection(1)"
    >
      Pie Chart
    </button>
    <button
      class="ui yellow tertiary button"
      @click="setSelection(2)"
    >
      3D Chart
    </button>
    <button
      class="ui olive tertiary button"
      @click="setSelection(3)"
    >
      Line Chart
    </button>
    <br/>
    <div>
      <ChartLoaderVue :selectChart="'BarChartVue'" v-show="graphNumber == 0" />
      <ChartLoaderVue :selectChart="'PieChartVue'" v-show="graphNumber == 1" />
      <ChartLoaderVue :selectChart="'Bar3DChartVue'" v-show="graphNumber == 2" />
      <ChartLoaderVue :selectChart="'LineChartVue'" v-show="graphNumber == 3" />
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
    },
    methods: {
      setSelection(graphNumber) {
        this.graphNumber = graphNumber;
        $cookies.set("selectedGraph", graphNumber);
      },
      initSelection() {
        if ($cookies.isKey("selectedGraph")) {
          this.graphNumber = $cookies.get("selectedGraph")
        } else {
          this.graphNumber = 0;
          $cookies.set("selectedGraph", 0, "1d");
        }
      }
    },
    created() {
      this.initSelection()
    }
  }
</script>
