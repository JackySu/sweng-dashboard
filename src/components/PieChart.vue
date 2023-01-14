<template>
  <div>
    <div class="chart" ref="pie" id="pieChart"></div>
  </div>
</template>
<script>
import * as echarts from 'echarts'
import axios from 'axios'
export default {
  data() {
    return {
      option: null,
    }
  },
  myChart: null,
  methods: {
    showEcharts() {
      let promise = new Promise((resolve, reject) => {
        this.myChart = echarts.init(this.$refs.pie, null, { renderer: 'svg' });
        this.option = {
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
          series: [{
            type: "pie",
            avoidLabelOverlap: false,
            "name": "Contributor commits",
            "clockwise": true,
            "data": [],
            "radius": [
              "30%",
              "65%"
            ],
            "center": [
              "50%",
              "50%"
            ],
            roseType: "radius",
            labelLine: {
              show: true
            },
            tooltip: {
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
              "formatter": "{a}<br/>{b}: {c} ({d}%)",
              "textStyle": {
                "fontSize": 14
              },
              "borderWidth": 0,
              "padding": 5,
            },
            "rippleEffect": {
              "show": true,
              "brushType": "stroke",
              "scale": 2.5,
              "period": 4
            }
          }],
          "title": [{
            "text": "Contribution Graph",
            "left": "center",
            "bottom": 20,
            "padding": 5,
            "itemGap": 10,
            "textStyle": {
              "color": "#000"
            }
          }],
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
        };
        this.myChart.setOption(this.option);
        const path = 'stats/contributors';
        axios.get(path, { params: {owner: $cookies.get('REPO_OWNER'), name: $cookies.get('REPO_NAME')}})
          .then((result) => {
            this.myChart.setOption({
              series: [{
                data: result.data.proportions,
              }],
              legend: [{
                data: result.data.legends,
              }],
            });
            this.option = this.myChart.getOption();
            this.myChart.on('finished',() => { resolve(); });
          })
          .catch((error) => {
            console.error(error);
          });
      });
      promise.then(() => {
        console.log("Finished loading PieChart");
        this.$emit('loaded', true);
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