// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
// import 'element-ui/lib/theme-chalk/index.css';//引用初始element-ui的css样式，如没有样式会丢失
import './assets/css/RegularText/theme/index.css' //RegularText 自定义风格主题
import ElementUI from 'element-ui';

import html from '../src/lib/html' //Ajax 请求拦截器
import store from './store'
import VueCookies from 'vue-cookies'


// import {setCookie,getCookie,delCookie} from './assets/js/cookie'

// Vue.prototype.$cookieStore = {setCookie,getCookie,delCookie}
Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(VueCookies)

//自定义Ajax 请求拦截器
var h=html.webService();
Vue.prototype.$axios = h

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>'
})
