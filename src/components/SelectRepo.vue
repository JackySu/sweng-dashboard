<template>
  <form class="ui form" id="selectRepo" @submit.prevent="selectRepo">
      <div class="two fields">
        <div class="field" id="end_date">
          <label>Repository name</label>

          <div class="ui input left icon">
            <i class="calendar icon"></i>
            <input name="repo_name" type="text" placeholder="Repo Name">
          </div>
        </div>
        <div class="field" style="margin-top: 25px;">
          <button type="submit" class="ui teal right labeled icon button">
            <i class="github icon"></i>
            Filter
          </button>
        </div>
      </div>
    </form>
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
      let parameters = {
        repo_name: form.elements.repo_name.value
      }
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
          console.log(result.data)
        })
        .catch((error) => {
          console.log(error)
        });
    }
  }
}
</script>