<template>
  <img src="../assets/icon.png" id="icon" />
  <h1>🅶🅸🆃<br/>🆁🅴🅿🅾</h1>
  <h2>🅼🅴🆃🅴🆁</h2>
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
    width: 220px;
  }

  .text-gradient {
    background-image: linear-gradient(to right, #270805, #865454);
    -webkit-background-clip: text;
    color: transparent;
    font-size: 30px;
  }
</style>