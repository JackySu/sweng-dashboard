import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import VueCookies from 'vue-cookies'
import axios from 'axios'

const app = createApp(App)
app.mount('#app')
app.config.globalProperties.$cookies = VueCookies

if ($cookies.isKey('REPO_OWNER') && $cookies.isKey('REPO_NAME')) {
  console.log(`cookies found as ${$cookies.get('REPO_OWNER')}/${$cookies.get('REPO_NAME')}`);
} else {
  $cookies.set('REPO_OWNER', 'apache', '1d').set('REPO_NAME', 'echarts', '1d');
  console.log('cookies initialized as apache/echarts');
}

axios.defaults.baseURL = 'http://localhost:50060/';