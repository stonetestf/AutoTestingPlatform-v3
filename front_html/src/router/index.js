import Vue from 'vue'

import login from '@/components/views/Login/index'
import Home from '@/components/views/Home/Main'
import Choose from '@/components/views/Home/Choose'//主页面选择入口
import RouterPar from '@/components/views/Setting/Router/Main'//路由管理
import Role from '@/components/views/Setting/Role/Main'//角色管理
import UserTable from '@/components/views/Setting/UserTable/Main'//用户管理
import OperationalInfo from '@/components/views/Setting/OperationalInfo/Main'//登录日志


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
      {path: '/Setting/Router/Main',name: 'Main',component: RouterPar},
      {path: '/Setting/Role/Main',name: 'Main',component: Role},
      {path: '/Setting/UserTable/Main',name: 'Main',component: UserTable},
      {path: '/Setting/OperationalInfo/Main',name: 'Main',component: OperationalInfo},
       
     ]}
  ]
})
