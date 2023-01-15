<template>
  <div id="demo_container">
    <div>
      <IconPageVue />
      <SelectRepoVue @update_repo="updateRepo" />
      <button class="ui left attached button" @click="subPageNum=0">Charts</button>
      <button class="right attached ui button" @click="subPageNum=1">Intro</button>
    </div>
    <div></div>
    <div id="chart_page">
      <ChartItemVue v-show="subPageNum==0" ref="charts"/>
      <MarkdownBlockVue v-show="subPageNum==1" />
    </div>
  </div>
</template>

<script>
  import SelectRepoVue from './components/SelectRepo.vue';
  import ChartItemVue from './components/ChartItem.vue';
  import MarkdownBlockVue from './components/MarkdownBlock.vue';
  import IconPageVue from './components/IconPage.vue';
  export default {
    data() {
      return {
        subPageNum: 0,
      }
    },
    components: {
      SelectRepoVue, ChartItemVue, MarkdownBlockVue, IconPageVue
    },
    methods: {
      updateRepo(owner, name) {
        $cookies.set('REPO_OWNER', owner, '1d').set('REPO_NAME', name, '1d');
        console.log(`update cookies as ${owner}/${name}`);
        this.$refs.charts.reloadAllCharts();
      }
    }
  }
</script>

<style scoped>
  #chart_page {
    padding-top: 40px;
    width: 1000px;
    height: 600px;
  }
  #demo_container {
    display: inline-grid;
    grid-template-columns: 300px 30px 1000px;
    grid-template-rows: repeat(2, 50%);
  }
</style>
