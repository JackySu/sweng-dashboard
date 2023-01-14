<template>
  <div>
    <div class="chart" ref="bar" id="barChart"></div>
  </div>
</template>
<script>
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
      let promise = new Promise((resolve, reject) => {
        this.myChart = echarts.init(this.$refs.bar, null, { renderer: 'svg' });
        this.option = {
          "series": [{
            "type": "bar",
            "name": "Additions",
            "legendHoverLink": true,
            "data": [],
            "showBackground": false,
            "stack": "stack1",
            "barMinHeight": 0,
            "barCategoryGap": "30%",
            "barGap": "30%",
            "large": false,
            "largeThreshold": 400,
            "seriesLayoutBy": "column",
            "datasetIndex": 0,
            "clip": true,
            "zlevel": 0,
            "z": 2,
            "label": {
              "show": true,
              "position": "top",
              "margin": 8
            },
            "itemStyle": {
              "color": "#FFBF00"
            }
          }, {
            "type": "bar",
            "name": "Deletions",
            "legendHoverLink": true,
            "data": [],
            "showBackground": false,
            "stack": "stack1",
            "barMinHeight": 0,
            "barCategoryGap": "30%",
            "barGap": "30%",
            "large": false,
            "largeThreshold": 400,
            "seriesLayoutBy": "column",
            "datasetIndex": 0,
            "clip": true,
            "zlevel": 0,
            "z": 2,
            "label": {
              "show": true,
              "position": "bottom",
              "margin": 8
            },
            "itemStyle": {
              "color": "#5484AB"
            }
          }],
          "legend": [{
            "data": ["Additions", "Deletions"],
            "selected": {
              "Additions": true,
              "Deletions": true
            },
            "show": true,
            "padding": 5,
            "itemGap": 10,
            "itemWidth": 25,
            "itemHeight": 14
          }],
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
          "toolbox": {
            "show": true,
            "orient": "horizontal",
            "itemSize": 15,
            "itemGap": 10,
            "left": "80%",
            "feature": {
              "saveAsImage": {
                "type": "png",
                "backgroundColor": "auto",
                "connectedBackgroundColor": "#fff",
                "show": true,
                "title": "保存为图片",
                "pixelRatio": 1
              },
              "dataView": {
                "show": true,
                "title": "数据视图",
                "readOnly": false,
                "lang": [
                  "数据视图",
                  "关闭",
                  "刷新"
                ],
                "backgroundColor": "#fff",
                "textareaColor": "#fff",
                "textareaBorderColor": "#333",
                "textColor": "#000",
                "buttonColor": "#c23531",
                "buttonTextColor": "#fff"
              },
              "magicType": {
                "show": true,
                "type": [
                  "line",
                  "bar",
                  "tiled"
                ],
                "title": {
                  "line": "切换为折线图",
                  "bar": "切换为柱状图",
                  "tiled": "切换为平铺"
                },
                "icon": {}
              },
            }
          },
          "xAxis": [{
            "show": true,
            "scale": false,
            "nameLocation": "end",
            "nameGap": 15,
            "gridIndex": 0,
            "inverse": false,
            "offset": 0,
            "splitNumber": 5,
            "minInterval": 0,
            "splitLine": {
              "show": false,
              "lineStyle": {
                "show": true,
                "width": 1,
                "opacity": 1,
                "curveness": 0,
                "type": "solid"
              }
            },
            "data": []
          }],
          "yAxis": [{
            "show": true,
            "scale": false,
            "nameLocation": "end",
            "nameGap": 15,
            "gridIndex": 0,
            "inverse": false,
            "offset": 0,
            "splitNumber": 5,
            "minInterval": 0,
            "splitLine": {
              "show": false,
              "lineStyle": {
                "show": true,
                "width": 1,
                "opacity": 1,
                "curveness": 0,
                "type": "solid"
              }
            }
          }],
          "title": [{
            "padding": 5,
            "itemGap": 10
          }],
          "dataZoom": {
            "show": true,
            "type": "slider",
            "realtime": true,
            "start": 0,
            "end": 10,
            "orient": "horizontal",
            "zoomLock": false,
            "filterMode": "filter"
          }
        };
        this.myChart.setOption(this.option);
        this.updateChart();

        this.myChart.on('finished',() => {
          resolve();
        })
      });
      promise.then(() => {
        console.log("Finished loading BarChart");
        this.$emit('loaded', true);
      });
    },
    updateChart() {
      const path = 'stats/code_frequency';
      axios.get(path, { params: {owner: $cookies.get('REPO_OWNER'), name: $cookies.get('REPO_NAME')}})
        .then((result) => {
          this.myChart.setOption({
            xAxis: {
              data: result.data.timeline,
            },
            series: [{
              data: result.data.addition,
            }, {
              data: result.data.deletion,
            }]
          });
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
    this.$emit('loaded', false);
    this.showEcharts();
  }
}
</script>