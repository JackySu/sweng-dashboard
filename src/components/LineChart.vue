<template>
  <div>
    <div class="chart" ref="line" id="lineChart"></div>
  </div>
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
      option: null,
    }
  },
  myChart: null,
  methods: {
    showEcharts() {
      let promise = new Promise((resolve, reject) => {
        this.myChart = echarts.init(this.$refs.line, null, { renderer: 'svg' });
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
              "type": "line",
              "name": "CPU Usage",
              "connectNulls": false,
              "symbolSize": 4,
              "showSymbol": true,
              "smooth": true,
              "clip": true,
              "step": false,
              "data": [
                []
              ],
              "hoverAnimation": true,
              "label": {
                "show": false,
                "position": "top",
                "margin": 8,
                "formatter": '{@[1]}%'
              },
              "lineStyle": {
                "show": true,
                "width": 1,
                "opacity": 1,
                "curveness": 0,
                "type": "solid"
              },
              "areaStyle": {
                "opacity": 0
              },
              "markPoint": {
                "label": {
                  "show": true,
                  "position": "inside",
                  "color": "#fff",
                  "margin": 8
                },
                "data": [
                  {
                    "type": "max"
                  }
                ]
              },
              "markLine": {
                "silent": false,
                "precision": 2,
                "label": {
                  "show": true,
                  "position": "top",
                  "margin": 8
                },
                "data": [
                  {
                    "type": "average"
                  }
                ]
              },
              "zlevel": 0,
              "z": 0,
              "rippleEffect": {
                "show": true,
                "brushType": "stroke",
                "scale": 2.5,
                "period": 4
              }
            },
            {
              "type": "line",
              "name": "RAM Usage",
              "connectNulls": false,
              "symbolSize": 4,
              "showSymbol": true,
              "smooth": true,
              "clip": true,
              "step": false,
              "data": [
                []
              ],
              "hoverAnimation": true,
              "label": {
                "show": false,
                "position": "top",
                "margin": 8,
                "formatter": "{@[1]}%"
              },
              "lineStyle": {
                "show": true,
                "width": 1,
                "opacity": 1,
                "curveness": 0,
                "type": "solid"
              },
              "areaStyle": {
                "opacity": 0
              },
              "markPoint": {
                "label": {
                  "show": true,
                  "position": "inside",
                  "color": "#fff",
                  "margin": 8
                },
                "data": [
                  {
                    "type": "max"
                  }
                ]
              },
              "markLine": {
                "silent": false,
                "precision": 2,
                "label": {
                  "show": true,
                  "position": "top",
                  "margin": 8
                },
                "data": [
                  {
                    "type": "average"
                  }
                ]
              },
              "zlevel": 0,
              "z": 0,
              "rippleEffect": {
                "show": true,
                "brushType": "stroke",
                "scale": 2.5,
                "period": 4
              }
            }
          ],
          "legend": [
            {
              "data": [
                "CPU Usage",
                "RAM Usage"
              ],
              "selected": {
                "CPU Usage": true,
                "RAM Usage": true
              },
              "show": true,
              "left": "50%",
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
          "xAxis": [
            {
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
              "data": [
                []
              ]
            }
          ],
          "yAxis": [
            {
              "type": "value",
              "show": true,
              "scale": false,
              "nameLocation": "end",
              "nameGap": 15,
              "gridIndex": 0,
              "axisTick": {
                "show": true,
                "alignWithLabel": false,
                "inside": false
              },
              "inverse": false,
              "offset": 0,
              "splitNumber": 5,
              "max": 100,
              "minInterval": 20,
              "splitLine": {
                "show": true,
                "lineStyle": {
                  "show": true,
                  "width": 1,
                  "opacity": 1,
                  "curveness": 0,
                  "type": "solid"
                }
              }
            }
          ],
          "title": [
            {
              "text": "Resources Monitor",
              "left": "10%",
              "padding": 5,
              "itemGap": 10
            }
          ],
          "toolbox": {
            "show": false,
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
              "restore": {
                "show": true,
                "title": "还原"
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
              "dataZoom": {
                "show": true,
                "title": {
                  "zoom": "区域缩放",
                  "back": "区域缩放还原"
                },
                "icon": {},
                "xAxisIndex": false,
                "yAxisIndex": false,
                "filterMode": "filter"
              },
              "magicType": {
                "show": true,
                "type": [
                  "line",
                  "bar",
                  "stack",
                  "tiled"
                ],
                "title": {
                  "line": "切换为折线图",
                  "bar": "切换为柱状图",
                  "stack": "切换为堆叠",
                  "tiled": "切换为平铺"
                },
                "icon": {}
              },
              "brush": {
                "icon": {},
                "title": {
                  "rect": "矩形选择",
                  "polygon": "圈选",
                  "lineX": "横向选择",
                  "lineY": "纵向选择",
                  "keep": "保持选择",
                  "clear": "清除选择"
                }
              }
            }
          },
          "dataZoom": {
            "show": true,
            "type": "slider",
            "realtime": true,
            "start": 0,
            "end": 100,
            "orient": "horizontal",
            "zoomLock": false,
            "filterMode": "filter"
          }
        };
        this.myChart.setOption(this.option);
        this.cpu_data = this.myChart.getOption().series[0].data;
        this.ram_data = this.myChart.getOption().series[1].data;
        this.updateData();
        this.cpu_data.shift();
        this.ram_data.shift();

        this.myChart.on('finished',() => {
          resolve();
        })
      });
      promise.then(() => {
        console.log("Finished loading LineChart");
        this.$emit('loaded', true);
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
          this.option = this.myChart.getOption();
        })
        .catch((error) => {
          console.error(error)
        });
    },
  },
  mounted() {
    this.$emit('loaded', false);
    this.showEcharts();
    this.update();
  }
}
</script>
