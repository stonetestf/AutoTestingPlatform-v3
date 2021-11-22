import Vue from 'vue'

import login from '@/components/views/Login/index'
import Home from '@/components/views/Home/Main'
import Choose from '@/components/views/Home/Choose'//主页面选择入口


import Router from 'vue-router'
Vue.use(Router)

// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题
const originalPush = Router.prototype.push
Router.prototype.push = function push (location) {
  return originalPush.call(this, location).catch(err => err)
}

export default new Router({
  mode: 'history',//去掉URL中的#/
  routes: [
    {path: '/',name: 'login',component: login},
     //Home页面
     {path: '/Main',name: 'Home',component: Home,children:[
      {path: '/Choose',name: 'Choose',component: Choose},
       
     ]}
  ]
})
