import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import VueCookies from 'vue-cookies'

const app = createApp(App)
app.mount('#app')
app.config.globalProperties.$cookies = VueCookies

if ($cookies.get('REPO_OWNER') !== undefined && $cookies.get('REPO_NAME') !== undefined) {
  console.log('cookies found');
} else {
  $cookies.set('REPO_OWNER', 'apache', '1d').set('REPO_NAME', 'echarts', '1d');
  console.log('cookies initialized as apache/echarts');
}

