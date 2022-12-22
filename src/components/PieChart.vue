<template>
  <div class="chart" ref="pie" initOpts="initOpts"></div>
</template>
<script scoped>
import * as echarts from 'echarts'
import axios from 'axios'
export default {
  data() {
    return {
      initOpts: {
        renderer: 'svg'
      },
      option: null,
    }
  },
  myChart: null,
  methods: {
    showEcharts() {
      this.myChart = echarts.init(this.$refs.pie, null, { renderer: 'svg' });
      const path = 'http://localhost:5000/stats/contributors';
      axios.get(path)
        .then((result) => {
          this.option = result.data;
          this.myChart.setOption(this.option);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  },
  mounted() {
    this.showEcharts();
  }
}
</script>