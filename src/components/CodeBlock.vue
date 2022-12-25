<template>
  <div id="code">
    <pre><code class="language-py line-numbers">{{ code }}</code></pre>
  </div>
</template>

<script scoped>
import * as prism from '../prism.js'
export default {
  data() {
    return {
      code: `import requests
headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': 'Bearer {GITHUB_TOKEN}',
}

response = requests.get('https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/{REPO_CATEGORY}', headers=headers)
with open('test.json', 'wb') as f:
    f.write(response.content)
`
    }
  },
  components: { prism }
}
</script>

<style scoped>
  #code {
    width: 100%;
  }
</style>