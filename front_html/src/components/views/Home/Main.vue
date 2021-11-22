<template>
  <div ref="tab-main">
    <template>
      <el-container>
        <el-header class="top-header">
          <el-row>
            <el-col :span="20">
              <el-menu
                mode="horizontal"
                @select="handleSelect"
                background-color="#545c64"
                text-color="#fff"
                active-text-color="#ffd04b">
                <el-menu-item index="0" >
                  <template slot="title" >
                    <i class="el-icon-star-off"></i>
                    <a>Home</a>
                  </template>
                </el-menu-item>
                <!-- <el-submenu index="3" :disabled="MenuDisPlqy.SmallTools">
                  <template slot="title">
                    <i class="el-icon-setting"></i>
                    <a>小工具</a>
                  </template>
                    <el-menu-item
                      class="title"
                      v-for="item in MenuList.SmallTools"
                      :index="item.index" :key="item.menuName"
                      >{{item.menuName}}
                    </el-menu-item>
                </el-submenu>
                <el-submenu index="2" :disabled="MenuDisPlqy.Setting">
                  <template slot="title">
                    <i class="el-icon-setting"></i>
                    <a>设置</a>
                  </template>
                    <el-menu-item
                      class="title"
                      v-for="item in MenuList.Setting"
                      :index="item.index" :key="item.menuName"
                      >{{item.menuName}}
                    </el-menu-item>
                </el-submenu> -->
              </el-menu>
            </el-col>
            <el-col :span="4">
              <div class="top-msg">
                <div style="margin-top: 5px;">
                <el-avatar :size="50" fit="fill" :src="RomeData.userImage"></el-avatar>
                </div>
                <div class="top-userName">
                  <el-dropdown trigger="click" @command="handleCommand">
                    <span style="color:white">{{RomeData.nickName}}
                      <i class="el-icon-caret-bottom el-icon--right"></i>
                    </span>
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item command="userinfo">个人信息</el-dropdown-item>
                      <el-dropdown-item command="close">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>
                </div>
              </div>
            </el-col>
          </el-row>
        </el-header>
        <el-main class="down-main">
          <div>
            <!-- 留坑，非常重要 -->
            <router-view></router-view>
          </div>
        </el-main>
      </el-container>
    </template>
    <template>
      <dialog-user-info
          @closeDialog="closeDialog_UserInfo" 
          :isVisible="dialog.userinfo.dialogVisible" 
          :dialogPara="dialog.userinfo.dialogPara">
      </dialog-user-info>
    </template>
  </div>
</template>

<script>
import store from '../../../store/index'
import {PrintConsole} from "../../js/Logger.js";
import DialogUserInfo from "./UserInfo.vue";

  export default {
    components: {
      DialogUserInfo
    },
    data() {
        return {
          RomeData:{
            nickName:'',
            userImage:'',
          },
          dialog:{
            userinfo:{
              dialogVisible:false,
              dialogPara:{
                dialogTitle:"",//初始化标题
              },
            }
          },
        }
    },
    mounted (){
      this.LoadUserInfo();
    },
    watch:{
    },
    methods: {
      handleSelect(key, keyPath) {//点击菜单跳转页面
        PrintConsole(key,keyPath);
        let self = this;
        if(key=='0'){
          self.$router.push('/Choose');
        }
      },
      QuitUser(){
        this.$cookies.remove('token');
        this.$router.push({ path:'/'  })
      },
      handleCommand(command){
        let self = this;
        if (command=="close"){
          self.QuitUser();
        }
        else if(command=="userinfo"){
          self.OpenDialog_UserInfo();
        }
      },
      closeDialog_UserInfo(){
        this.dialog.userinfo.dialogVisible =false;
      },
      OpenDialog_UserInfo(){
          let self = this;
          self.dialog.userinfo.dialogPara={
            dialogTitle:"个人信息",//初始化标题
          }
          self.dialog.userinfo.dialogVisible=true;
      },
      LoadUserInfo(){//基本信息及权限信息
        let self = this;
        self.$axios.get('/api/home/LoadUserInfo', {
          params:{}
        }).then(res => {
          if(res.data.statusCode==2000){
            this.$cookies.set('nickName',res.data.baseInfo.nickName,"0") 
            self.RomeData.nickName =this.$cookies.get('nickName');
           
            if(res.data.baseInfo.userImg){
              store.state.userImage = res.data.baseInfo.userImg;
              self.RomeData.userImage = 'data:image/png;base64,'+store.state.userImage ;
            }
            self.$router.push('/Choose');
          }else{
            self.$message.error('用户数据获取失败:'+res.data.errorMsg);
          }
        }).catch(function (error) {
          console.log(error);
        })
      },
    }
  }

</script>

<style>
.top-header{
  background-color: #545c64
}
.down-main{
  border-radius: 0px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
  /* height: 870px; */
  /* background-color: rgb(235, 237, 240); */
}
.top-userName{
  margin-top: 20px;
  margin-left: 10px;
}
.top-msg{
  font-size: 12px;
  height: 60px;
  display: flex; 
  justify-content: flex-end; 
  background-color:#545c64;
}
</style>