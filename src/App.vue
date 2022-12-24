<script setup>
  import SelectRepoVue from './components/SelectRepo.vue';
  import ChartItemVue from './components/ChartItem.vue';
  import MarkdownBlockVue from './components/MarkdownBlock.vue';
  import IconPageVue from './components/IconPage.vue';
</script>

<template>
  <div id="demo_container">
    <div>
      <IconPageVue />
      <SelectRepoVue />
      <button class="ui left attached button" @click="subPageNum=0">Charts</button>
      <button class="right attached ui button" @click="subPageNum=1">Intro</button>
    </div>
    <div></div>
    <div id="chart_page">
      <ChartItemVue v-show="subPageNum==0"/>
      <MarkdownBlockVue v-show="subPageNum==1"/>
    </div>
  </div>
</template>

<script scoped>
  export default {
    data() {
      return {
        subPageNum: 0,
      }
    },
    components: {
      SelectRepoVue, ChartItemVue, MarkdownBlockVue, IconPageVue
    }
  }
</script>

<style scoped>
  #chart_page {
    width: 1000px;
    height: 600px;
  }
  #demo_container {
    display: inline-grid;
    grid-template-columns: 25% 30px 75%;
    grid-template-rows: repeat(2, 50%);
  }
</style>
