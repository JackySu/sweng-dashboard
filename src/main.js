import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import VueCookies from 'vue-cookies'

const app = createApp(App)
app.mount('#app')
app.config.globalProperties.$cookies = VueCookies

let owner = $cookies.get('REPO_OWNER');
let name = $cookies.get('REPO_NAME');
if (owner !== undefined && name !== undefined) {
  console.log(`cookies found as ${owner}/${name}`);
} else {
  $cookies.set('REPO_OWNER', 'apache', '1d').set('REPO_NAME', 'echarts', '1d');
  console.log('cookies initialized as apache/echarts');
}

