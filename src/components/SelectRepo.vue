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
            <div v-show="resultsDisplay" class="results"></div>
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
      repoNames: [],
      resultsDisplay: false,
    }
  },
  methods: {
    selectRepo() {
      if (this.repoNames.length == 0) {
        return;
      }
      console.log(this.repoNames)
      const full_name = this.repoNames[0].title.split('/');
      this.$emit('update_repo', full_name[0], full_name[1]);
    },
    searchRepo() {
      let form = document.querySelector('#selectRepo');
      let keyword = form.elements.repo_name.value;
      const path = `https://api.github.com/search/repositories?q=${keyword}`;
      this.resultsDisplay = false;
      axios.get(path)
        .then((result) => {
          let results = result.data.items.slice(0, 10);
          this.repoNames = [];
          for (var repo of results) {
            this.repoNames.push({
              title: repo.full_name
            });
          }
          this.resultsDisplay = true;
          $('.ui.search')
            .search({
              source: this.repoNames,
              searchFullText: true,
              maxResults: 5,
          });
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
    document.getElementsByName('repo_name')[0].addEventListener('change', (event) => {
      this.searchRepo();
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