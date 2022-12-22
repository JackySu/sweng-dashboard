<template>
  <div class="chart" ref="line" initOpts="initOpts"></div>
</template>

<script scoped>
import * as echarts from 'echarts'
import axios from 'axios'
export default {
  data() {
    return {
      cpu_data: [],
      ram_data: [],
      x_axis: [],
      timer: null,
      maxDataListLength: 30,
    }
  },
  myChart: null,
  methods: {
    showEcharts() {
      this.myChart = echarts.init(this.$refs.line, null, { renderer: 'svg' });
      const path = 'http://localhost:5000/lineChart';
      axios.get(path)
        .then((result) => {
          this.myChart.setOption(result.data);
          this.cpu_data = this.myChart.getOption().series[0].data;
          this.ram_data = this.myChart.getOption().series[1].data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    update() {
      this.timer = setInterval(() => {
        // this.myChart.dispose();
        // this.showEcharts();
        this.updateData();
      }, 2000)
    },
    updateData() {
      const path = 'http://localhost:5000/lineDynamicData';
      axios.get(path)
        .then((result) => {
          this.cpu_data.push([result.data.name, result.data.cpu_usage]);
          this.ram_data.push([result.data.name, result.data.ram_usage]);
          this.x_axis.push(result.data.name);
          if (this.x_axis.length > this.maxDataListLength) {
            this.cpu_data.shift();
            this.ram_data.shift();
            this.x_axis.shift();
          }
          this.myChart.setOption({
            xAxis: {
              data: this.x_axis,
            },
            series: [{
              data: this.cpu_data
            }, {
              data: this.ram_data
            }]
          });
        })
        .catch((error) => {
          console.error(error)
        });
    },
  },
  mounted() {
    this.showEcharts();
    this.update();
  }
}
</script>
