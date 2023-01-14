<template>
  <div style="position: relative" >
    <component :is="selectChart" @loaded="setDisplay"></component>
    <div v-show="!isChartDisplayed" class="loadingio-spinner-ellipsis-9jvoq1er23r">
      <div class="ldio-5vf2fuygssf">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
  </div>
</template>

<script>
  import LineChartVue from "./LineChart.vue"
  import BarChartVue from "./BarChart.vue"
  import PieChartVue from "./PieChart.vue"
  import Bar3DChartVue from "./Bar3DChart.vue"
  export default {
    data() {
      return {
        isChartDisplayed: false,
      }
    },
    components: {
      LineChartVue, BarChartVue, PieChartVue, Bar3DChartVue
    },
    methods: {
      setDisplay(result) {
        this.isChartDisplayed = result;
      }
    },
    props: {
      selectChart: {
        type: String,
        required: true
      }
    },
  }
</script>