<template>
  <div id="introduction">
    <md-block>{{ blockContent }}</md-block>
    <br/>
    <CodeBlockVue />
    <div class="text-divider">Tech Stack</div>
    <div>
      <a class="ui blue tertiary button" href="https://www.python.org/"><i
        class="python icon"></i>Python</a>
      <a class="ui red tertiary button" href="https://echarts.apache.org/"><i
        class="chart area icon"></i>Echarts</a>
      <a class="ui teal tertiary button" href="https://vuejs.org/"><i
        class="paint vuejs icon"></i>Vue</a>
    </div>
  </div>
</template>

<script>
import {MarkdownBlock, MarkdownSpan, MarkdownElement} from "md-block";
import CodeBlockVue from "./CodeBlock.vue";
export default {
  data() {
    return {
      blockContent: `## Measuring changes
A modern visualization method revealing the trend among the stats of repositories

## Source of Data
All the data of the repo is fetched from the [GitHub Rest API](https://docs.github.com/en/rest)
With **Python** as our back-end solution, we retrieve the data we want with simple steps`,
      
    }
  },
  components: {
    MarkdownBlock, MarkdownSpan, MarkdownElement, CodeBlockVue
  }
}
</script>

<style scope>
  #introduction {
    width: 100%;
  }
  md-block {
    width: 100%;
  }
</style>