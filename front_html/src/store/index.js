import Vue from 'vue'
import Vuex from 'vuex'//引入vuex
// import createPersistedState from "vuex-persistedstate" //刷新也不会清除vuex信息

Vue.use(Vuex); //使用 vuex
const store = new Vuex.Store({
  
  // 如果此刻想配置多个选项，将plugins写成一个一维数组，不然会报错,刷新也不会清除vuex信息
//   plugins:[createPersistedState()],
  state: {
    isDebug:true,
    userId:"",
    // nickName:"",
    // userImage:'',
    // tokenValue: "",
    
    //测试
    // userName:'',
    // passWord:'',

    //开发
    userName:'admin',
    passWord:'hbwj@123',
    
    BackService:'http://127.0.0.1:9090',
  },
  mutations: {
    // userId(state,payload){
    //   state.userId = payload;
    // }
  }
})

export default store