<template>
  <div>
    <form class="ui form" id="selectRepo" @submit.prevent="selectRepo">
      <div class="two fields">
        <div class="field">
          <label>repository name</label>
          <div class="ui search">
            <div class="ui input left icon">
              <i class="edit icon"></i>
              <input id="repo_name" class="prompt" name="repo_name" type="text" placeholder="Repo Name">
            </div>
            <div class="results"></div>
          </div>
        </div>
        <div class="field">
          <button type="submit" class="ui black tertiary button">
            <i class="github icon" style="padding-top: 35px"></i>
            Select
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
    }
  },
  methods: {
    selectRepo() {
      let form = document.querySelector('#selectRepo');
      let keyword = form.elements.repo_name.value;
      const path = `searchRepo?keyword=${keyword}`;
      axios.get(path)
        .then((res) => {
          let results = res.data.result;
          let repoNames = [];
          for (var repo of results) {
            repoNames.push({
              title: repo.title,
            });
          }
          if (repoNames.length == 0) {
            return;
          }
          console.log(repoNames);
          const full_name = repoNames[0].title.split('/');
          this.$emit('update_repo', full_name[0], full_name[1]);
          // location.reload(); // refresh whole page
        })
        .catch((error) => {
          console.log(error)
        });
      /*
      const path = 'http://localhost:5000/selectRepo';
      axios.post(path, parameters, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        transformRequest: [(data) => {
          let ret = '';
          for (let i in data) {
            ret += `${encodeURIComponent(i)}=${encodeURIComponent(data[i])}&`;
          }
        return ret;
        }]
      })
        .then((result) => {
          console.log("Spectate on repo " + result.data);
          document.querySelector('#repo_name').value=result.data;
        })
        .catch((error) => {
          console.log(error)
        });
      */
    },
    getReferRepos() {
      let content = '';
      for (let repo of this.repoNames) {
        content += `${repo}\n`;
      }
      return content;
    }
  },
  mounted() {
    $('.ui.search')
      .search({
        apiSettings: {
          url: 'http://localhost:5085/searchRepo?keyword={query}',
        },
        fields: {
          results: 'result',
          title: 'title',
          url: '#',
        },
        minCharacters: 2,
        maxResults: 5,
    });
  }
}
</script>

<style scoped>
  #selectRepo {
    width: 400px;
  }
  label {
    padding: 5px;
  }
</style>