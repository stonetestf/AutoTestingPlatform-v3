import Vue from 'vue'

import login from '@/components/views/Login/index'
import Home from '@/components/views/Home/Main'
import Choose from '@/components/views/Home/Choose'//主页面选择入口
import RouterPar from '@/components/views/Setting/Router/Main'//路由管理
import Role from '@/components/views/Setting/Role/Main'//角色管理
import UserTable from '@/components/views/Setting/UserTable/Main'//用户管理
import OperationalInfo from '@/components/views/Setting/OperationalInfo/Main'//登录日志
import Notice from '@/components/views/Setting/Notice/Main'//公告

//API 接口
import ApiHome from '@/components/views/SysType/Api/Home'
import Api_ProjectManagement from '@/components/views/SysType/Api/ProjectManagement/Main'

import ApiPageHome from '@/components/views/SysType/Api/Page/Home'
import ApiPageMain from '@/components/views/SysType/Api/Page/Main'
import Api_PageManagement from '@/components/views/SysType/Api/Page/PageManagement/Main';//所属页面
import Api_FunManagement from '@/components/views/SysType/Api/Page/FunManagement/Main';//所属功能
import Api_WorkorderMaintenance from '@/components/views/WorkorderManagement/WorkorderMaintenance/Main';//工单维护
import Api_ApiMaintenance from '@/components/views/SysType/Api/Page/CaseManagement/ApiMaintenance/Main';//接口维护
import Api_PageEnvironment from '@/components/views/SysType/Api/Page/EnvironmentalManagement/PageEnvironment/Main';//页面环境
import Api_GlobalVariable from '@/components/views/SysType/Api/Page/EnvironmentalManagement/GlobalVariable/Main';//全局变量
import Api_DebugTalk from '@/components/views/SysType/Api/Page/Setting/DebugTalk/Main';//DebugTalk.py
import Api_RemindInfo from '@/components/views/WorkorderManagement/RemindInfo/Main';//提醒消息
import Api_TestReport from '@/components/views/SysType/Api/Page/TestReport/Main';//测试报告主页
import Api_Report from '@/components/views/SysType/Api/Page/TestReport/Report';//测试报告
import Api_CaseMaintenance from '@/components/views/SysType/Api/Page/CaseManagement/CaseMaintenance/Main';//用例维护
import Api_TimingTask from '@/components/views/SysType/Api/Page/TaskManagement/TimingTask/Main';//定时任务
import Api_BatchTask from '@/components/views/SysType/Api/Page/TaskManagement/BatchTask/Main';//批量任务
import Api_SystemParams from '@/components/views/SysType/Api/Page/Setting/SystemParams/Main';//系统参数
import Api_DataBase from '@/components/views/SysType/Api/Page/EnvironmentalManagement/DataBase/Main';//数据库环境

//UI 功能
import UiHome from '@/components/views/SysType/Ui/Home'
import Ui_ProjectManagement from '@/components/views/SysType/Ui/ProjectManagement/Main'

import UiPageHome from '@/components/views/SysType/Ui/Page/Home'
import UiPageMain from '@/components/views/SysType/Ui/Page/Main'
import Ui_PageManagement from '@/components/views/SysType/Ui/Page/PageManagement/Main';//所属页面
import Ui_FunManagement from '@/components/views/SysType/Ui/Page/FunManagement/Main';//所属功能
import Ui_ElementMaintenance from '@/components/views/SysType/Ui/Page/CaseManagement/ElementMaintenance/Main';//元素维护
import Ui_ElementEvent from '@/components/views/SysType/Ui/Page/Setting/ElementEvent/Main';//元素类型


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
    {path: '/SysType/Api/Page/TestReport/Report',name: 'Api_Report',component: Api_Report},
    //Home页面
    {path: '/Main',name: 'Home',component: Home,
      children:[
        {path: '/Choose',name: 'Choose',component: Choose},
        {path: '/Setting/Router/Main',name: 'Main',component: RouterPar},
        {path: '/Setting/Role/Main',name: 'Main',component: Role},
        {path: '/Setting/UserTable/Main',name: 'Main',component: UserTable},
        {path: '/Setting/OperationalInfo/Main',name: 'Main',component: OperationalInfo},
        {path: '/Setting/Notice/Main',name: 'Main',component: Notice},
      ]
    },
    //API入口
    {path: '/SysType/Api/Home',name: 'ApiHome',component: ApiHome,
      children:[
        {path: '/SysType/Api/ProjectManagement/Main',name: 'Api_ProjectManagement',component: Api_ProjectManagement,
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
        {path: '/WorkorderManagement/WorkorderMaintenance/Main',name: 'Api_WorkorderMaintenance',component: Api_WorkorderMaintenance,
          meta:{name: '工单维护',url:'/WorkorderManagement/WorkorderMaintenance/Main',comp:'Api_WorkorderMaintenance'}
        },
        {path: '/SysType/Api/Page/CaseManagement/ApiMaintenance/Main',name: 'Api_ApiMaintenance',component: Api_ApiMaintenance,
          meta:{name: '接口维护',url:'/SysType/Api/Page/CaseManagement/ApiMaintenance/Main',comp:'Api_ApiMaintenance'}
        },
        {path: '/SysType/Api/Page/EnvironmentalManagement/PageEnvironment/Main',name: 'Api_PageEnvironment',component: Api_PageEnvironment,
          meta:{name: '页面环境',url:'/SysType/Api/Page/EnvironmentalManagement/PageEnvironment/Main',comp:'Api_PageEnvironment'}
        },
        {path: '/SysType/Api/Page/EnvironmentalManagement/GlobalVariable/Main',name: 'Api_GlobalVariable',component: Api_GlobalVariable,
          meta:{name: '全局变量',url:'/SysType/Api/Page/EnvironmentalManagement/GlobalVariable/Main',comp:'Api_GlobalVariable'}
        },
        {path: '/SysType/Api/Page/Setting/DebugTalk/Main',name: 'Api_PageEnvironment',component: Api_DebugTalk,
          meta:{name: 'DebugTalk.py',url:'/SysType/Api/Page/Setting/DebugTalk/Main',comp:'Api_DebugTalk'}
        },
        {path: '/WorkorderManagement/RemindInfo/Main',name: 'Api_RemindInfo',component: Api_RemindInfo,
          meta:{name: '提醒消息',url:'/WorkorderManagement/RemindInfo/Main',comp:'Api_RemindInfo'}
        },
        {path: '/SysType/Api/Page/TestReport/Main',name: 'Api_TestReport',component: Api_TestReport,
          meta:{name: '报告维护',url:'/SysType/Api/Page/TestReport/Main',comp:'Api_TestReport'}
        },
        {path: '/SysType/Api/Page/CaseManagement/CaseMaintenance/Main',name: 'Api_CaseMaintenance',component: Api_CaseMaintenance,
          meta:{name: '用例维护',url:'/SysType/Api/Page/CaseManagement/CaseMaintenance/Main',comp:'Api_CaseMaintenance'}
        },
        {path: '/SysType/Api/Page/TaskManagement/TimingTask/Main',name: 'Api_TimingTask',component: Api_TimingTask,
          meta:{name: '定时任务',url:'/SysType/Api/Page/TaskManagement/TimingTask/Main',comp:'Api_TimingTask'}
        },
        {path: '/SysType/Api/Page/TaskManagement/BatchTask/Main',name: 'Api_BatchTask',component: Api_BatchTask,
          meta:{name: '批量任务',url:'/SysType/Api/Page/TaskManagement/BatchTask/Main',comp:'Api_BatchTask'}
        },
        {path: '/SysType/Api/Page/Setting/SystemParams/Main',name: 'Api_SystemParams',component: Api_SystemParams,
          meta:{name: '系统参数',url:'/SysType/Api/Page/Setting/SystemParams/Main',comp:'Api_SystemParams'}
        },
        {path: '/SysType/Api/Page/EnvironmentalManagement/DataBase/Main',name: 'Api_DataBase',component: Api_DataBase,
          meta:{name: '数据库环境',url:'/SysType/Api/Page/EnvironmentalManagement/DataBase/Main',comp:'Api_DataBase'}
        },
      ]
    },
    //UI入口
    {path: '/SysType/Ui/Home',name: 'UiHome',component: UiHome,
      children:[
        {path: '/SysType/Ui/ProjectManagement/Main',name: 'Ui_ProjectManagement',component: Ui_ProjectManagement,
        },
      ]
    },
    {path: '/SysType/Ui/Page/Home',name: 'UiPageHome',component: UiPageHome,
    children:[
      {path: '/SysType/Ui/Page/Main',name: 'UiPageMain',component: UiPageMain},
      {path: '/SysType/Ui/Page/PageManagement/Main',name: 'Ui_PageManagement',component: Ui_PageManagement,
        meta:{name: '页面维护',url:'/SysType/Ui/Page/PageManagement/Main',comp:'Ui_PageManagement'}
      },
      {path: '/SysType/Ui/Page/FunManagement/Main',name: 'Ui_FunManagement',component: Ui_FunManagement,
        meta:{name: '功能维护',url:'/SysType/Ui/Page/FunManagement/Main',comp:'Ui_FunManagement'}
      },
      {path: '/SysType/Ui/Page/CaseManagement/ElementMaintenance/Main',name: 'Ui_ElementMaintenance',component: Ui_ElementMaintenance,
        meta:{name: '元素维护',url:'/SysType/Ui/Page/CaseManagement/ElementMaintenance/Main',comp:'Ui_ElementMaintenance'}
      },
      {path: '/SysType/Ui/Page/Setting/ElementEvent/Main',name: 'Ui_ElementEvent',component: Ui_ElementEvent,
        meta:{name: '元素事件维护',url:'/SysType/Ui/Page/Setting/ElementEvent/Main',comp:'Ui_ElementEvent'}
      },
    ]
  },
  ]
})
