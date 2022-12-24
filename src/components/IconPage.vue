<template>
  <img src="../assets/icon.png" id="icon" />
  <h1 class="text-gradient">Git Repo Analysis</h1>
  <p>An echarts solution with Python + Vue.js</p>
  <div class="text-divider">Choose Repo</div>
</template>

<script>
import { MarkdownBlock, MarkdownSpan, MarkdownElement } from "md-block";
export default {
  data() {
    return {
    }
  },
  components: {
    MarkdownBlock, MarkdownSpan, MarkdownElement
  }
}
</script>

<style scope>
  #icon {
    width: 280px;
  }

  .text-gradient {
    background-image: linear-gradient(to right, #ffc17a, #270805, #f3f3f3);
    -webkit-background-clip: text;
    color: transparent;
    font-size: 30px;
  }
</style>