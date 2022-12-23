<template>
  <div>
    <div class="chart" ref="bar" id="barChart"></div>
  </div>
</template>
<script scoped>
import * as echarts from 'echarts'
import axios from 'axios'
export default {
  data() {
    return {
      timer: null,
      option: null,
    }
  },
  myChart: null,
  methods: {
    showEcharts() {
      this.myChart = echarts.init(this.$refs.bar, null, { renderer: 'svg' });
      const path = 'http://localhost:5000/stats/code_frequency';
      axios.get(path)
        .then((result) => {
          this.option = result.data;
          this.myChart.setOption(this.option);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    reloadChart() {
      this.myChart.dispose();
      this.showEcharts();
    }
  },
  mounted() {
    this.showEcharts();
  }
}
</script>