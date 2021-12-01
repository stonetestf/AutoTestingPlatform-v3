import Vue from 'vue'

import login from '@/components/views/Login/index'
import Home from '@/components/views/Home/Main'
import Choose from '@/components/views/Home/Choose'//主页面选择入口
import RouterPar from '@/components/views/Setting/Router/Main'//路由管理
import Role from '@/components/views/Setting/Role/Main'//角色管理
import UserTable from '@/components/views/Setting/UserTable/Main'//用户管理
import OperationalInfo from '@/components/views/Setting/OperationalInfo/Main'//登录日志

//API 接口
import ApiHome from '@/components/views/SysType/Api/Home'
import ApiMain from '@/components/views/SysType/Api/Main'
import Api_ProjectManagement from '@/components/views/SysType/Api/ProjectManagement/Main'

import ApiPageHome from '@/components/views/SysType/Api/Page/Home'
import ApiPageMain from '@/components/views/SysType/Api/Page/Main'
import Api_PageManagement from '@/components/views/SysType/Api/Page/PageManagement/Main';
import Api_FunManagement from '@/components/views/SysType/Api/Page/FunManagement/Main';


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
    {path: '/Main',name: 'Home',component: Home,
      children:[
        {path: '/Choose',name: 'Choose',component: Choose},
        {path: '/Setting/Router/Main',name: 'Main',component: RouterPar},
        {path: '/Setting/Role/Main',name: 'Main',component: Role},
        {path: '/Setting/UserTable/Main',name: 'Main',component: UserTable},
        {path: '/Setting/OperationalInfo/Main',name: 'Main',component: OperationalInfo},
      ]
    },
    //API入口
    {path: '/SysType/Api/Home',name: 'ApiHome',component: ApiHome,
      children:[
        {path: '/SysType/Api/Main',name: 'ApiMain',component: ApiMain},
        {path: '/SysType/Api/ProjectManagement/Main',name: 'Api_ProjectManagement',component: Api_ProjectManagement,
          meta:{name: '项目维护',url:'/SysType/Api/ProjectManagement/Main',comp:'Api_ProjectManagement'}
        },
      ]
    },
    //API主体
    {path: '/SysType/Api/Page/Home',name: 'ApiPageHome',component: ApiPageHome,
      children:[
        {path: '/SysType/Api/Page/Main',name: 'ApiPageMain',component: ApiPageMain},
        {path: '/SysType/Api/Page/PageManagement/Main',name: 'Api_PageManagement',component: Api_PageManagement,
          meta:{name: '页面维护',url:'/SysType/Api/Page/PageManagement/Main',comp:'Api_PageManagement'}
        },
        {path: '/SysType/Api/Page/FunManagement/Main',name: 'Api_FunManagement',component: Api_FunManagement,
          meta:{name: '功能维护',url:'/SysType/Api/Page/FunManagement/Main',comp:'Api_FunManagement'}
        },
      ]
    }
  ]
})
