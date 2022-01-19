<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="11">
                <el-card style="height:850px">
                    <div>
                        <div>
                            <el-card shadow="never" style="height:100px">
                                <el-row>
                                    <el-col :span="6">
                                        <el-row>
                                            <el-col :span="12">
                                                <div>
                                                    <el-image
                                                        style="margin:0px -10px 0px 0px;float:right;width: 60px; height: 60px"
                                                        :src="IconImg.user"
                                                        fit="cover">
                                                    </el-image>
                                                </div>
                                            </el-col>
                                            <el-col :span="12">
                                                <div>用户总数</div>
                                                <div class="leftTotal">1</div>
                                            </el-col>
                                        </el-row>
                                    </el-col>
                                    <el-col :span="6">
                                        <el-row>
                                            <el-col :span="12">
                                                <div>
                                                    <el-image
                                                        style="margin:5px -10px 0px 0px;float:right;width: 50px; height: 50px"
                                                        :src="IconImg.cases"
                                                        fit="cover">
                                                    </el-image>
                                                </div>
                                            </el-col>
                                            <el-col :span="12">
                                                <div>用例总数</div>
                                                <div class="leftTotal">1</div>
                                            </el-col>
                                        </el-row>
                                    </el-col>
                                    <el-col :span="6">
                                       <el-row>
                                            <el-col :span="12">
                                                <div>
                                                    <el-image
                                                        style="margin:5px -10px 0px 0px;float:right;width: 50px; height: 50px"
                                                        :src="IconImg.tasks"
                                                        fit="cover">
                                                    </el-image>
                                                </div>
                                            </el-col>
                                            <el-col :span="12">
                                                <div>任务总数</div>
                                                <div class="leftTotal">1</div>
                                            </el-col>
                                        </el-row>
                                    </el-col>
                                    <el-col :span="6">
                                        <el-row>
                                            <el-col :span="12">
                                                <div>
                                                    <el-image
                                                        style="margin:5px -10px 0px 0px;float:right;width: 50px; height: 50px"
                                                        :src="IconImg.total"
                                                        fit="cover">
                                                    </el-image>
                                                </div>
                                            </el-col>
                                            <el-col :span="12">
                                                <div>执行总数</div>
                                                <div class="leftTotal">1</div>
                                            </el-col>
                                        </el-row>
                                    </el-col>
                                </el-row>
                            </el-card>
                        </div>
                        <div style="margin-top:10px">
                            <el-card shadow="never" style="height:350px">
                                
                            </el-card>
                        </div>
                    </div>
                    <div style="margin-top:10px">
                        <el-card style="height:350px" shadow="never">
                            <span v-if="RomeData.noticeTime">公告:【{{RomeData.noticeTime}}】</span>
                            <span v-else>公告</span>
                            <div style="margin-top:10px;text-align:left;overflow:auto;height:290px;">
                                <span style="white-space: pre-line;" v-html="RomeData.notice"></span>
                            </div>
                        </el-card>
                    </div>

                </el-card>
            </el-col>
            <el-col :span="13">
                <el-card style="height:850px">
                    <div style="margin-left:65px">
                        <el-row :gutter="290">
                            <el-col :span="4">
                                <el-card class="btn" shadow="hover" @click.native="handleClick('API')">
                                    <el-image
                                        style="width: 150px; height: 150px"
                                        :src="IconImg.api"
                                        fit="cover">
                                    </el-image>
                                    <div class="btn-text">接口测试</div>
                                </el-card>
                            </el-col>
                            <el-col :span="4">
                                <el-card class="btn" shadow="hover" @click.native="handleClick('UI')">
                                    <el-image
                                        style="width: 150px; height: 150px"
                                        :src="IconImg.ui"
                                        fit="cover">
                                    </el-image>
                                    <div class="btn-text">功能测试(建设中)</div>
                                </el-card>
                            </el-col>
                            <el-col :span="4">
                                <el-card class="btn" shadow="hover" @click.native="handleClick('')">
                                    <el-image
                                        style="width: 150px; height: 150px"
                                        :src="IconImg.pts"
                                        fit="cover">
                                    </el-image>
                                    <div class="btn-text">梯度测试(建设中)</div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </div>
                </el-card>
            </el-col>
        </el-row>
     </div>
</template>
<script>
import {PrintConsole} from "../../js/Logger.js";
import store from '../../../store/index.js';

import api from '@/assets/images/Choose/API.png';
import ui from '@/assets/images/Choose/UI.png';
import pts from '@/assets/images/Choose/PTS.png';

import user from '@/assets/images/Choose/USER.png';
import cases from '@/assets/images/Choose/CASE.png';
import tasks from '@/assets/images/Choose/TASK.png';
import total from '@/assets/images/Choose/TOTAL.png';
// var echarts = require('echarts');


  export default {
    data() {
      return {
        IconImg:{
            api:api,
            ui:ui,
            pts:pts,

            user:user,
            cases:cases,
            tasks:tasks,
            total:total
        },
        RomeData:{
            notice:'',//公告
            noticeTime:'',
        },
        // ServerPerformance:{
        //     socket:'',
        //     myChartCPU:'',
        //     myChartMEM:'',
        //     celery:'exception',//异步服务
        //     celeryBeat:'exception',//定时任务服务
        // },
      };
    },
    beforeDestroy(){//生命周期-离开时
        // this.ServerPerformance.socket.close(); //关闭TCP连接
    },
    mounted(){
        // this.ServerPerformance.myChartCPU = echarts.init(document.getElementById('cpuIndicators'));//初始化
        // this.ServerPerformance.myChartMEM = echarts.init(document.getElementById('memIndicators'));//初始化

        // this.CpuIndicators(0);
        // this.MemIndicators(0);
        // this.CreateSocket();
        this.SelectNoticeInfo();

    },
    methods: {
        // //监控类
        // CpuIndicators(val){
        //     let self = this;
        //     // var myChartCPU = echarts.init(document.getElementById('cpuIndicators'));//初始化
        //     var option = {
        //         series: [
        //             {
        //             type: 'gauge',
        //                 axisLine: {
        //                     lineStyle: {
        //                     width: 30,
        //                     color: [
        //                         [0.3, '#67e0e3'],
        //                         [0.7, '#37a2da'],
        //                         [1, '#fd666d']
        //                     ]
        //                     }
        //                 },
        //                 pointer: {
        //                     itemStyle: {
        //                     color: 'auto'
        //                     }
        //                 },
        //                 axisTick: {
        //                     distance: -30,
        //                     length: 8,
        //                     lineStyle: {
        //                     color: '#fff',
        //                     width: 2
        //                     }
        //                 },
        //                 splitLine: {
        //                     distance: -30,
        //                     length: 30,
        //                     lineStyle: {
        //                     color: '#fff',
        //                     width: 4
        //                     }
        //                 },
        //                 axisLabel: {
        //                     color: 'auto',
        //                     distance: 40,
        //                     fontSize: 15
        //                 },
        //                 detail: {
        //                     fontSize: 18,
        //                     valueAnimation: true,
        //                     formatter: 'CPU {value} %',
        //                     color: 'auto'
        //                 },
        //                 data: [
        //                     {
        //                         value: val
        //                     }
        //                 ]
        //             }
        //         ]
        //     };
        //     self.ServerPerformance.myChartCPU.setOption(option,true);//加载属性后显示 true自动每次清除数据
        // },
        // MemIndicators(val){
        //     let self = this;
        //     var option = {
        //         series: [
        //             {
        //             type: 'gauge',
        //                 axisLine: {
        //                     lineStyle: {
        //                     width: 30,
        //                     color: [
        //                         [0.3, '#67e0e3'],
        //                         [0.7, '#37a2da'],
        //                         [1, '#fd666d']
        //                     ]
        //                     }
        //                 },
        //                 pointer: {
        //                     itemStyle: {
        //                     color: 'auto'
        //                     }
        //                 },
        //                 axisTick: {
        //                     distance: -30,
        //                     length: 8,
        //                     lineStyle: {
        //                     color: '#fff',
        //                     width: 2
        //                     }
        //                 },
        //                 splitLine: {
        //                     distance: -30,
        //                     length: 30,
        //                     lineStyle: {
        //                     color: '#fff',
        //                     width: 4
        //                     }
        //                 },
        //                 axisLabel: {
        //                     color: 'auto',
        //                     distance: 40,
        //                     fontSize: 15
        //                 },
        //                 detail: {
        //                     fontSize: 18,
        //                     valueAnimation: true,
        //                     formatter: 'MEM {value} %',
        //                     color: 'auto'
        //                 },
        //                 data: [
        //                     {
        //                         value: val
        //                     }
        //                 ]
        //             }
        //         ]
        //     };
        //     self.ServerPerformance.myChartMEM.setOption(option,true);//加载属性后显示 true自动每次清除数据
        // },
        // CreateSocket(){//创建socket连接 获取数据 这里获取2个服务器
        //     let self = this;
        //     var socket = new WebSocket(store.state.WebSock+'/api/home/GetServerIndicators');
        //     self.ServerPerformance.socket = socket;
            
        //     socket.onopen = function () {
        //         // PrintConsole('WebSocket open');//成功连接上Websocket
        //         var data ={};
        //         data.Message = 'Start';
        //         data.Params = {
        //             'token':self.$cookies.get('token')
        //         }
        //         socket.send(JSON.stringify(data));//发送数据到服务端
        //     };
        //     socket.onmessage = function (e) {
        //         PrintConsole('message: ' + e.data);//打印服务端返回的数据
        //         let retData = JSON.parse(e.data)
        //         self.CpuIndicators(retData.cpu);
        //         self.MemIndicators(retData.mem);

        //         var data ={};
        //         data.Message = 'Heartbeat';
        //         data.Params = {
        //             'time':'Date()'
        //         }
        //         socket.send(JSON.stringify(data));//发送数据到服务端
        //         //celery服务
        //         if(retData.celery){
        //             self.ServerPerformance.celery = 'success';
        //         }else{
        //             self.ServerPerformance.celery = 'exception';
        //         }
        //         if(retData.celeryBeat){
        //             self.ServerPerformance.celeryBeat = 'success';
        //         }else{
        //             self.ServerPerformance.celeryBeat = 'exception';
        //         }
        //     };
        //     socket.onclose=function(e){
        //         PrintConsole("关闭TCP连接onclose",e);
        //         socket.close(); //关闭TCP连接
        //         // //10次重连
        //         // for(let i=1;i<=11;i++){
        //         //     PrintConsole("正在重连",i);
        //         //     self.CreateSocket();
        //         // }
        //     };
        //     if (socket.readyState == WebSocket.OPEN) socket.onopen();       
        // },
        SelectNoticeInfo(){
            let self = this;
            self.$axios.get('/api/Notice/SelectNewNotice',{
                params:{

                }
            }).then(res => {
               if(res.data.statusCode==2000){
                   self.RomeData.noticeTime = res.data.noticeTime;
                   self.RomeData.notice = res.data.notice;
               }else{
                   self.$message.error('公告信息获取失败:'+res.data.errorMsg);
               }
            }).catch(function (error) {
                console.log(error);
            })
        },

        handleClick(val){//跳转类
            if(val=='API'){
                this.$router.push({path:'/SysType/Api/Home'});
            }else if(val=='UI'){

            }
        },
    }
  };
</script>

<style>
.btn-text{
    font-size: 30px;
}
.btn{
    height: 250px;
    width: 250px;
}
.btn-div{
    margin-top: 15%;
    
}
.leftTotal{
    font-size: 25px;
    margin-top: 10px;
}
</style>
