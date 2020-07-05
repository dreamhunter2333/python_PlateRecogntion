import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import axios from 'axios'
// Vue.prototype.$axios = axios
// axios.defaults.baseURL = ''
// axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';

// Vue.use(axios)
Vue.use(ElementUI)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
