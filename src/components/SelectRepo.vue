
<template>
  <div>
    <form class="ui form" id="selectRepo" @submit.prevent="selectRepo">
      <div class="two fields">
        <div class="field">
          <label>Repository name</label>
          <div class="ui input left icon">
            <i class="edit icon"></i>
            <input id="repo_name" name="repo_name" type="text" placeholder="Repo Name">
          </div>
        </div>
        <div class="field" style="margin-top: 25px;">
          <button type="submit" class="ui black tertiary button">
            <i class="github icon"></i>
            Select
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script scoped>
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
      const path = `https://api.github.com/search/repositories?q=${keyword}`;
      axios.get(path)
        .then((result) => {
          const full_name = result.data.items[0].full_name.split('/');
          $cookies.set('REPO_OWNER', full_name[0], '1d').set('REPO_NAME', full_name[1], '1d');
          location.reload();
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
    }
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