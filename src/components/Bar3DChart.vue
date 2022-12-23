<template>
  <div>
    <div class="chart" ref="bar3d" id="b3dChart"></div>
    <form class="ui form" id="filterForm" @submit.prevent="getFiltered">
      <div class="three fields">
        <div class="field" id="start_date">
          <label>Start date</label>
          <div class="ui calendar" id="rangestart">
            <div class="ui input left icon">
              <i class="calendar icon"></i>
              <input name="start" type="text" placeholder="Start">
            </div>
          </div>
        </div>
        <div class="field" id="end_date">
          <label>End date</label>
          <div class="ui calendar" id="rangeend">
            <div class="ui input left icon">
              <i class="calendar icon"></i>
              <input name="end" type="text" placeholder="End">
            </div>
          </div>
        </div>
        <div class="field" style="margin-top: 25px;">
          <button type="submit" class="ui yellow right labeled icon button">
            <i class="search icon"></i>
            Filter
          </button>
        </div>
      </div>
    </form>
  </div>
</template>
<script scoped>
import * as echarts from 'echarts'
import 'echarts-gl'
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
      let promise = new Promise((resolve, reject) => {
        this.myChart = echarts.init(this.$refs.bar3d, null, { renderer: 'canvas'});
        const path = 'http://localhost:5000/filter_commits';
        axios.get(path)
          .then((result) => {
            this.option = result.data;
            this.myChart.setOption(this.option);
          })
          .catch((error) => {
            console.error(error);
          });
          this.myChart.on('finished',() => {
          resolve();
        })
      });
      promise.then(() => {
        console.log("Finished loading Bar3DChart");
        this.$emit('loaded', true);
      });
    },
    showCalendar() {
      $('#rangestart').calendar({
        type: 'date',
        formatter: {
          date: 'YYYY-MM-DD'
        },
        endCalendar: $('#rangeend')
      });
      $('#rangeend').calendar({
        type: 'date',
        formatter: {
          date: 'YYYY-MM-DD'
        },
        startCalendar: $('#rangestart')
      });
    },
    getFiltered() {
      let form = document.querySelector('#filterForm');
      let parameters = {
        start: form.elements.start.value,
        end: form.elements.end.value
      }
      const path = 'http://localhost:5000/filter_commits';
      axios.get(path, { params: parameters})
        .then((result) => {
          this.option = result.data;
          this.myChart.setOption(this.option);
        });
    },
    reloadChart() {
      this.myChart.dispose();
      this.showEcharts();
    }
  },
  mounted() {
    this.$emit('loaded', false);
    this.showEcharts();
    this.showCalendar();  
  }
}
</script>