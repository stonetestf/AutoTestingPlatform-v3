import Vue from 'vue'
import Vuex from 'vuex'//引入vuex
import createPersistedState from "vuex-persistedstate" //刷新也不会清除vuex信息

Vue.use(Vuex); //使用 vuex
const store = new Vuex.Store({
  // 如果此刻想配置多个选项，将plugins写成一个一维数组，不然会报错,刷新也不会清除vuex信息
  plugins:[createPersistedState()],
  state: {
    isDebug:true,
    userImage:'',
    version:'211122',
    // userImage:'',
    
    //测试
    // userName:'',
    // passWord:'',

    //开发
    userName:'admin',
    passWord:'hbwj@123',
    
    BackService:'http://192.168.2.12:9090',
    nginxUrl:'http://192.168.2.12:9092/',// 注意这里的端口不是网页的端口，是网络目录的地址
    WebSock:'ws://192.168.2.12:9090',
  },
  mutations: {
    //vueX 不能直接赋值，必须在这里声明
    userImage(state,payload){
      state.userImage = payload;
    }
  }
})

export default store