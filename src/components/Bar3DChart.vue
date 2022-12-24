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
        this.myChart = echarts.init(this.$refs.bar3d, null, { renderer: 'canvas' });
        this.option = {
          "animation": true,
          "animationThreshold": 2000,
          "animationDuration": 1000,
          "animationEasing": "cubicOut",
          "animationDelay": 0,
          "animationDurationUpdate": 300,
          "animationEasingUpdate": "cubicOut",
          "animationDelayUpdate": 0,
          "color": [
            "#c23531",
            "#2f4554",
            "#61a0a8",
            "#d48265",
            "#749f83",
            "#ca8622",
            "#bda29a",
            "#6e7074",
            "#546570",
            "#c4ccd3",
            "#f05b72",
            "#ef5b9c",
            "#f47920",
            "#905a3d",
            "#fab27b",
            "#2a5caa",
            "#444693",
            "#726930",
            "#b2d235",
            "#6d8346",
            "#ac6767",
            "#1d953f",
            "#6950a1",
            "#918597"
          ],
          "series": [
            {
              "type": "bar3D",
              "name": "Commits",
              "data": [],
              "label": {
                "show": false,
                "position": "top",
                "margin": 8
              },
              "rippleEffect": {
                "show": true,
                "brushType": "stroke",
                "scale": 2.5,
                "period": 4
              },
              "tooltip": {
                "show": true,
                "trigger": "item",
                "triggerOn": "mousemove|click",
                "axisPointer": {
                  "type": "line"
                },
                "showContent": true,
                "alwaysShowContent": false,
                "showDelay": 0,
                "hideDelay": 100,
                "formatter": "{a} made {b}<br\>on {c} times",
                "textStyle": {
                  "fontSize": 14
                },
                "borderWidth": 0,
                "padding": 5
              }
            }
          ],
          "legend": [
            {
              "data": [
                "Commits"
              ],
              "selected": {
              },
              "show": true,
              "padding": 5,
              "itemGap": 10,
              "itemWidth": 25,
              "itemHeight": 14
            }
          ],
          "tooltip": {
            "show": true,
            "trigger": "item",
            "triggerOn": "mousemove|click",
            "axisPointer": {
              "type": "line"
            },
            "showContent": true,
            "alwaysShowContent": false,
            "showDelay": 0,
            "hideDelay": 100,
            "textStyle": {
              "fontSize": 14
            },
            "borderWidth": 0,
            "padding": 5
          },
          "visualMap": {
            "show": true,
            "type": "continuous",
            "min": 0,
            "max": 20,
            "inRange": {
              "color": [
                "#50a3ba",
                "#eac763",
                "#d94e5d"
              ]
            },
            "calculable": true,
            "inverse": false,
            "splitNumber": 5,
            "orient": "vertical",
            "showLabel": true,
            "itemWidth": 20,
            "itemHeight": 140,
            "borderWidth": 0
          },
          "xAxis3D": {
            "nameGap": 20,
            "type": "category",
            "axisLabel": {
              "margin": 8
            }
          },
          "yAxis3D": {
            "data": [],
            "nameGap": 20,
            "type": "category",
            "axisLabel": {
              "margin": 8
            }
          },
          "zAxis3D": {
            "nameGap": 20,
            "type": "value",
            "axisLabel": {
              "margin": 8
            }
          },
          "grid3D": {
            "boxWidth": 200,
            "boxHeight": 100,
            "boxDepth": 80,
            "viewControl": {
              "autoRotate": false,
              "autoRotateSpeed": 10,
              "rotateSensitivity": 1
            }
          },
          "title": [
            {
              "text": "Commits Heatmap",
              "padding": 30,
              "itemGap": 10
            }
          ]
        };
        this.myChart.setOption(this.option);

        const path = 'http://localhost:5000/filter_commits';
        axios.get(path)
          .then((result) => {
            this.myChart.setOption({
              series: [{
                data: result.data.result
              }],
              yAxis3D: {
                data: result.data.names
              }
            });
            this.option = this.myChart.getOption();
          })
          .catch((error) => {
            console.error(error);
          });
        this.myChart.on('finished', () => {
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
      axios.get(path, { params: parameters })
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
<style scoped>
  #b3dchart {
    padding-left: 30px;
  }
</style>