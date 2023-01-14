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
    <div v-if="isChartShow">
      <ChartLoaderVue v-for="item in items" :key="item.index" :selectChart="item.component" v-show="graphNumber == item.index" />
    </div>
  </div>
</template>

<script>
  import ChartLoaderVue from './ChartLoader.vue';
  export default {
    data() {
      return {
        graphNumber: 0,
        isChartShow: true,
        items: [
          {
            index: "0",
            component: "BarChartVue"
          },
          {
            index: "1",
            component: "PieChartVue"
          },
          {
            index: "2",
            component: "Bar3DChartVue"
          },
          {
            index: "3",
            component: "LineChartVue"
          }
        ]
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
      },
      reloadAllCharts() {
        this.isChartShow = false;
        this.$nextTick(() => {
          this.isChartShow = true;
        });
      }
    },
    created() {
      this.initSelection()
    }
  }
</script>
