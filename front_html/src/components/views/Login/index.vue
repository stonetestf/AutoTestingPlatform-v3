<template>
  <div ref="tab-main"  class="RomeData">
    <template>
      <h3 style="margin-left:70px">ATesting</h3>
      <el-form :model="RomeData"  :rules="RomeData.rules" ref="RomeData" label-width="100px">
        <el-form-item label="用户名" prop="userName">
            <el-input placeholder="请输入用户名" v-model="RomeData.userName"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="passWord">
          <el-input  placeholder="请输入密码" show-password v-model="RomeData.passWord"  @keyup.enter.native="loginIn()"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="LoginIn()">登录</el-button>
          <el-button @click="OpenEditDialog_registered()">注册</el-button>
        </el-form-item>
      </el-form>
    </template>
    <template>
      <dialog-registered
        @closeDialog="closeDialog_registered" 
        :isVisible="dialog.registered.dialogVisible" 
        :dialogPara="dialog.registered.dialogPara">
      </dialog-registered>
    </template>
  </div>
</template>

<script>
import Qs from 'qs'
import store from '../../../store/index'
import DialogRegistered from "./Registered";

export default {
  components: {
      DialogRegistered,
  },
  data() {
    return {
      RomeData: {
        userName:store.state.userName,
        passWord:store.state.passWord,
        rules: {
          userName: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
          passWord: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
          ],
        },
      },
      dialog:{
        registered:{//注册信息
          dialogVisible:false,
          dialogPara:{
            dialogTitle:"",//初始化标题
            isAddNew:true,//初始化是否新增\修改
          },
        },
      },
    };
  },
  mounted(){

  },
  methods: {
    resetForm(formName) {//清除正则验证
      if (this.$refs[formName] !== undefined) {
          this.$refs[formName].resetFields();
      }
    },
    closeDialog_registered(){
      this.dialog.registered.dialogVisible =false;
    },
    OpenEditDialog_registered(){
      this.dialog.registered.dialogPara={
        dialogTitle:'用户注册',//初始化标题
        isAddNew:true,//初始化是否新增\修改
      }
      this.dialog.registered.dialogVisible=true;
    },
    LoginIn(){
        let self = this;
        self.$axios.post('/api/login/loginIn',
        Qs.stringify({
            'userName':self.RomeData.userName,
            'passWord':self.RomeData.passWord,
        })).then(res => {
          if(res.data.statusCode==2000){
              self.$store.commit("userId",res.data.userId)//把用户id信息放到vuex中
              // this.$cookieStore.setCookie( 'token' ,res.data.tokenValue, 60);//存入用户名，设置有效时间1分钟,意味着一分钟后cookie自动消失。一天为 86400 s
              this.$cookies.set('token',res.data.tokenValue,"0") //0的意思是随浏览器关闭就没了,但不能同时开2个浏览器,这里是浏览器不是窗口的意思,如果开2个 只有2个都关了才会没有
              // this.$cookies.set('userId',res.data.userId)

              self.$router.push({//跳转到
                name:'Home',
                params:{
                  userId:res.data.userId,
                }
              })
          }
          else{
              this.$message.error(res.data.errorMsg);
          } 
        })
    },
  }
}
</script>
<style>
.RomeData{
    margin:0 auto;
    width:400px;
    position: absolute;
    height:200px;
    left:50%;
    top:50%; 
    margin-left:-200px;
    margin-top:-100px;
} 
</style>
