<template>
  <div ref="tab-main"  id="tab-main">
    <template>
      <el-card class="MainCard">
          <!-- <span>这里显示当前项目的接口数量，单元测试数量，测试用例数量，定时任务数据，批量任务数量</span>
          <span>当前项目的成功，失败全统计</span>
          <span></span>
           <span></span> -->
          <div>
            <el-row :gutter="10">
              <el-col :span="11">
                <div>
                  <el-card class="TopCard">
                    <div id="topline" style="width:830px;height:300px;margin-left:-20px;"></div>   
                  </el-card>
                </div>
              </el-col>
              <el-col :span="13">
                <div>
                  <el-card class="TopCard">
                    <el-table
                      height="290px"
                      :data="RomeData.proTableData">
                      <el-table-column
                        prop="pageName"
                        align= "center"
                        label="所属页面">
                      </el-table-column>
                      <el-table-column
                        width="80px"
                        prop="apiTotal"
                        align= "center"
                        label="接口数量">
                      </el-table-column>
                      <el-table-column
                        width="80px"
                        prop="unitAndCaseTotal"
                        align= "center"
                        label="单元/混合">
                      </el-table-column>
                      <el-table-column
                        width="80px"
                        prop="caseTotal"
                        align= "center"
                        label="测试用例">
                      </el-table-column>
                      <el-table-column
                        width="80px"
                        prop="taskTotal"
                        align= "center"
                        label="定时任务">
                      </el-table-column>
                      <el-table-column
                        width="80px"
                        prop="batchTotal"
                        align= "center"
                        label="批量任务">
                      </el-table-column>
                      <el-table-column
                        width="80px"
                        prop="weekTotal"
                        align= "center"
                        label="本周新增">
                      </el-table-column>
                      <el-table-column
                        width="100px"
                        prop="performWeekTotal"
                        align= "center"
                        label="本周执行">
                      </el-table-column>
                      <el-table-column
                        width="100px"
                        prop="perforHistoryTotal"
                        align= "center"
                        label="历史执行">
                      </el-table-column>
                    </el-table>
                  </el-card>
                </div>
              </el-col>
            </el-row>
          </div>
          <div style="margin-top:10px">
            <el-row :gutter="10">
              <el-col :span="11">
                <div>
                  <el-card class="DownCard">
                    <div style="margin-top:-10px">
                      <el-tag type="info">过去7天内失败TOP 10 </el-tag>
                    </div>
                    <div style="margin-top:10px">
                      <el-table
                        height="330px"
                        :data="RomeData.formerlyTableData">
                        <el-table-column
                          prop="index"
                          width="70px"
                          align= "center"
                          label="排名">
                          <template slot-scope="scope">
                              <el-tag type="danger" v-if="scope.row.index=='1'" >{{scope.row.index}}</el-tag>
                              <el-tag type="warning" v-else-if="scope.row.index=='2'">{{scope.row.index}}</el-tag>
                              <el-tag type="primary" v-else-if="scope.row.index=='3'">{{scope.row.index}}</el-tag>
                              <span v-else>{{scope.row.index}}</span>
                          </template>
                        </el-table-column>
                        <el-table-column
                          prop="taskName"
                          align= "center"
                          label="任务名称">
                        </el-table-column>
                        <el-table-column
                          prop="itsName"
                          align= "center"
                          label="所属页面/功能">
                        </el-table-column>
                        <el-table-column
                          align= "center"
                          width="100px"
                          label="任务类型">
                          <template slot-scope="scope">
                              <el-tag v-if="scope.row.taskType=='API'" > 独立接口</el-tag>
                              <el-tag type="success" v-else-if="scope.row.taskType=='CASE'" >测试用例</el-tag>
                              <el-tag type="warning" v-else-if="scope.row.taskType=='TASK'" >定时任务</el-tag>
                              <el-tag type="danger" v-else-if="scope.row.taskType=='BATCH'" >批量任务</el-tag>
                          </template>
                        </el-table-column>
                        <el-table-column
                          prop="number"
                          align= "center"
                          width="100px"
                          label="失败次数">
                        </el-table-column>
                      </el-table>
                    </div>
                  </el-card>
                </div>
              </el-col>
              <el-col :span="13">
                <div>
                  <el-card class="DownCard">
                    <div style="margin-top:-10px">
                      <el-tag type="info">项目队列</el-tag>
                    </div>
                    <div style="margin-top:10px">
                      <el-table
                        height="330px"
                        :data="RomeData.queueTableData">
                        <el-table-column
                          prop="taskName"
                          align= "center"
                          label="任务名称">
                        </el-table-column>
                        <el-table-column
                          prop="itsName"
                          align= "center"
                          label="所属页面/功能">
                        </el-table-column>
                        <el-table-column
                          width="100px"
                          align= "center"
                          label="任务类型">
                          <template slot-scope="scope">
                              <el-tag v-if="scope.row.taskType=='API'" >接口</el-tag>
                              <el-tag type="success" v-else-if="scope.row.taskType=='CASE'" >测试用例</el-tag>
                              <el-tag type="warning" v-else-if="scope.row.taskType=='TASK'" >定时任务</el-tag>
                              <el-tag type="danger" v-else-if="scope.row.taskType=='BATCH'" >批量任务</el-tag>
                          </template>
                        </el-table-column>
                        <el-table-column
                          width="100px"
                          align= "center"
                          label="任务状态">
                          <template slot-scope="scope">
                              <el-tag type="info" v-if="scope.row.taskState=='0'" >未开始</el-tag>
                              <el-tag type="warning" v-else-if="scope.row.taskState=='1'" >执行中</el-tag>
                          </template>
                        </el-table-column>
                        <el-table-column
                          prop="performProgress"
                          width="100px"
                          align= "center"
                          label="执行进度">
                        </el-table-column>
                        <el-table-column
                          prop="updateTime"
                          width="100px"
                          align= "center"
                          label="发布时间">
                        </el-table-column>
                        <el-table-column
                          label="操作"
                          align="center"
                          width="80px">
                          <template slot-scope="scope" style="width:100px">
                            <el-button
                              type="info"
                              size="mini"
                              @click="handleState(scope.$index, scope.row)">取消
                            </el-button>
                        </template>
                      </el-table-column>
                      </el-table>
                    </div>
                  </el-card>
                </div>
              </el-col>
            </el-row>
          </div>
      </el-card>
    </template>
  </div>
</template>

<script>
import Qs from 'qs';
import * as echarts from 'echarts';
import store from '../../../../../store/index';
import {PrintConsole} from "../../../../js/Logger.js";

export default {
  components: {

  },
  data() {
    return {
        myChart_line:'',
        RomeData:{
          socket:'',
          topLine:{
            timeData:[],
            passData:[],
            failData:[],
            errorData:[],
          },
          //项目统计
          proTableData:[
            // {'itsName':'测试页面/测试功能','apiTotal':'1000000','unitTotal':'20','caseTotal':'13','taskTotal':'30','batchTotal':'20','weekTotal':"12",'performWeek':'11','perforHistory':'30'}
          ],
          //过去7天失败错误列表
          formerlyTableData:[
            // {'index':'1','itsName':'测试页面/测试功能','taskType':'API','taskName':'查询项目','number':'999'},
            // {'index':'2','itsName':'测试页面/测试功能','taskType':'CASE','taskName':'验证项目','number':'888'},
            // {'index':'3','itsName':'测试页面/测试功能','taskType':'TASK','taskName':'查询项目','number':'777'},
            // {'index':'4','itsName':'测试页面/测试功能','taskType':'BATCH','taskName':'验证项目','number':'666'},
          ],
          //队列列表
          queueTableData:[
            // {'itsName':'测试页面/测试功能','taskType':'API','taskName':'验证项目','taskState':'0','performProgress':'1/1'},
            // {'itsName':'测试页面/测试功能','taskType':'CASE','taskName':'验证项目','taskState':'1' ,'performProgress':'2/20'},
          ]

        },

    };
  },
  mounted(){
    this.myChart_line = echarts.init(document.getElementById('topline'));//初始化
    // this.topline();
    this.SelectTestResults();//测试结果总览
    this.SelectProStatistical();//项目统计
    this.SelectFormerlyData();//过去7天内Top10
    this.SelectProQueue();//项目队列

    this.PageMainDataRefresh();//当前页面的4块数据无感刷新
  },
  beforeDestroy(){//生命周期-离开时
    this.RomeData.socket.close(); //关闭TCP连接
  },
  methods: {
    SelectTestResults(){//测试结果总览
      let self = this;
      self.$axios.get('/api/home/ApiPageHomeSelectTestResults',{
        params:{
          'proId':self.$cookies.get('proId'),
        }
      }).then(res => {
        if(res.data.statusCode==2000){
          self.RomeData.topLine.timeData = res.data.timeData;
          self.RomeData.topLine.passData = res.data.passData;
          self.RomeData.topLine.failData = res.data.failData;
          self.RomeData.topLine.errorData = res.data.errorData;
          this.topline();
        }else{
            self.$message.error('获取数据失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
          console.log(error);
      })
    },
    topline(){
      let self = this;
      var option_line = {
        title: {
          text: '测试结果总览',
          left:'40'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['Pass', 'Fail', 'Error']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        // toolbox: {
        //   feature: {
        //     saveAsImage: {}
        //   }
        // },
        xAxis: {
          type: 'category',
          axisLabel: { interval: 0, rotate: 30 },//底部文字倾斜显示
          data:self.RomeData.topLine.timeData
          // data: ['Mon', 'Tue','123']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            label: {
              show: true,
              position: 'top'
            },
            name: 'Pass',
            type: 'bar',
            // stack: 'Total',
            data:self.RomeData.topLine.passData,
            // data: [
            //       {name:'2016/12/18 6:38:08', value:['2016/12/18 6:38:08', 20]},
            //       {name:'2016/12/18 16:18:18', value:['2016/12/18 16:18:18', 1]},
            //       {name:'2016/12/18 19:18:18', value:['2016/12/18 19:18:18', 1]}
            //   ],
            itemStyle: {normal: {color: '#91cc75'}} 
          },
          {
            label: {
              show: true,
              position: 'top'
            },
            name: 'Fail',
            type: 'bar',
            // stack: 'Total',
            data:self.RomeData.topLine.failData,
            // data: [
            //     {name:'2016/12/17 6:38:08', value:['2016/12/17 6:38:08', 1]},
            //     {name:'2016/12/17 16:18:18', value:['2016/12/17 16:18:18', 22]},
            //     {name:'2016/12/17 19:18:18', value:['2016/12/17 19:18:18', 44]}
            // ],
            itemStyle: {normal: {color: '#fac858'}} 
          },
          {
            label: {
              show: true,
              position: 'top'
            },
            name: 'Error',
            type: 'bar',
            // stack: 'Total',
            data:self.RomeData.topLine.errorData,
            // data: [
            //     {name:'2016/12/16 6:38:08', value:['2016/12/16 6:38:08', 1]},
            //     {name:'2016/12/16 16:18:18', value:['2016/12/16 16:18:18', 22]},
            //     {name:'2016/12/16 19:18:18', value:['2016/12/16 19:18:18', 44]}
            // ],
            itemStyle: {normal: {color: '#ee6666'}} 
          },
        ]
      };
      this.myChart_line.setOption(option_line,true);//加载属性后显示 true自动每次清除数据
    },
    SelectProStatistical(){//项目总览
      let self = this;
      self.$axios.get('/api/home/ApiPageHomeSelectProStatistical',{
        params:{
          'proId':self.$cookies.get('proId'),
        }
      }).then(res => {
        if(res.data.statusCode==2000){
          self.RomeData.proTableData = res.data.dataTable;
        }else{
          self.$message.error('获取数据失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
          console.log(error);
      })
    },
    SelectFormerlyData(){//过去7天内Top10
      let self = this;
      self.$axios.get('/api/home/ApiPageHomeSelectFormerlyData',{
        params:{
          'proId':self.$cookies.get('proId'),
        }
      }).then(res => {
        if(res.data.statusCode==2000){
          self.RomeData.formerlyTableData = res.data.dataTable;
        }else{
          self.$message.error('获取数据失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
          console.log(error);
      })
    },
    SelectProQueue(){//项目队列
      let self = this;
      self.$axios.get('/api/home/ApiPageHomeSelectProQueue',{
        params:{
          'proId':self.$cookies.get('proId'),
        }
      }).then(res => {
        if(res.data.statusCode==2000){
          self.RomeData.queueTableData = res.data.dataTable;
        }else{
          self.$message.error('获取数据失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
        console.log(error);
      })
    },
    handleState(index,row){//项目队列取消
      let self = this;
      self.$axios.post('/api/home/ApiPageHomeHandleState',Qs.stringify({
        'queueId':row.id,
      })).then(res => {
        if(res.data.statusCode==2002){
          self.SelectProQueue();
        }
        else{
          self.$message.error('队列状态修改失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
          console.log(error);
      })
    },
    PageMainDataRefresh(){//当前页面的4块数据无感刷新
      let self = this;
      var socket = new WebSocket(store.state.WebSock+'/api/home/ApiPageMainDataRefresh');
      self.RomeData.socket = socket;
      socket.onopen = function () {
        PrintConsole('WebSocket open');//成功连接上Websocket
        var data ={};
        data.Message = 'Start';
        data.Params = {
          'proId':self.$cookies.get('proId')
        }
        socket.send(JSON.stringify(data));//发送数据到服务端
      };
      socket.onmessage = function (e) {
        // PrintConsole('message: ' + e.data);//打印服务端返回的数据
        let retData = JSON.parse(e.data)
        //测试结果总览
        self.RomeData.topLine.timeData = retData.testResults.timeData;
        self.RomeData.topLine.passData = retData.testResults.passData;
        self.RomeData.topLine.failData = retData.testResults.failData;
        self.RomeData.topLine.errorData = retData.testResults.errorData;
        self.topline();

        //项目下统计数据
        retData.proStatistical.dataTable.forEach(d=>{
          let tempTable = self.RomeData.proTableData.find(item=>
            item.id == d.id
          );
          if(tempTable){
            //查看是不是有差异
            if(d.pageName!=tempTable.pageName){
              tempTable.pageName = d.pageName
            }
            if(d.apiTotal!=tempTable.apiTotal){
              tempTable.apiTotal = d.apiTotal
            }
            if(d.unitAndCaseTotal!=tempTable.unitAndCaseTotal){
              tempTable.unitAndCaseTotal = d.unitAndCaseTotal
            }
            if(d.caseTotal!=tempTable.caseTotal){
              tempTable.caseTotal = d.caseTotal
            }
            if(d.taskTotal!=tempTable.taskTotal){
              tempTable.taskTotal = d.taskTotal
            }
            if(d.batchTotal!=tempTable.batchTotal){
              tempTable.batchTotal = d.batchTotal
            }
            if(d.weekTotal!=tempTable.weekTotal){
              tempTable.weekTotal = d.weekTotal
            }
            if(d.performWeekTotal!=tempTable.performWeekTotal){
              tempTable.performWeekTotal = d.performWeekTotal
            }
            if(d.perforHistoryTotal!=tempTable.perforHistoryTotal){
              tempTable.perforHistoryTotal = d.perforHistoryTotal
            }

          }else{
            self.RomeData.proTableData.push(d);//新增数据
          }
        });
        //删除数据
        self.RomeData.proTableData.forEach((d,index)=>{
          let tempTable = retData.proStatistical.dataTable.find(item=>
            item.id == d.id
          );
          if(tempTable){

          }else{
            self.RomeData.proTableData.splice(index, 1)
          }
        });

        //过去7天内Top10
        retData.pastSevenDaysTop.dataTable.forEach(d=>{
          let tempTable = self.RomeData.formerlyTableData.find(item=>
            item.taskName == d.taskName
          );
          if(tempTable){
            //查看是不是有差异
            if(d.index!=tempTable.index){
              tempTable.index = d.index
            }
            if(d.taskName!=tempTable.taskName){
              tempTable.taskName = d.taskName
            }
            if(d.itsName!=tempTable.itsName){
              tempTable.itsName = d.itsName
            }
            if(d.taskType!=tempTable.taskType){
              tempTable.taskType = d.taskType
            }
            if(d.number!=tempTable.number){
              tempTable.number = d.number
            }
         

          }else{
            self.RomeData.formerlyTableData.push(d);//新增数据
          }
        });
        //删除数据
        self.RomeData.formerlyTableData.forEach((d,index)=>{
          let tempTable = retData.pastSevenDaysTop.dataTable.find(item=>
            item.taskName == d.taskName
          );
          if(tempTable){

          }else{
            self.RomeData.formerlyTableData.splice(index, 1)
          }
        });

        //项目队列
        retData.proQueue.dataTable.forEach(d=>{
          let tempTable = self.RomeData.queueTableData.find(item=>
            item.id == d.id
          );
          if(tempTable){
            //查看是不是有差异
            if(d.taskName!=tempTable.taskName){
              tempTable.taskName=d.taskName
            }
            if(d.itsName!=tempTable.itsName){
              tempTable.itsName=d.itsName
            }
            if(d.taskType!=tempTable.taskType){
              tempTable.taskType=d.taskType
            }
            if(d.taskState!=tempTable.taskState){
              tempTable.taskState=d.taskState
            }
            if(d.performProgress!=tempTable.performProgress){
              tempTable.performProgress=d.performProgress
            }
            if(d.updateTime!=tempTable.updateTime){
              tempTable.updateTime=d.updateTime
            }

          }else{
            self.RomeData.queueTableData.push(d);//新增数据
          }
        });
        //删除数据
        self.RomeData.queueTableData.forEach((d,index)=>{
          let tempTable = retData.proQueue.dataTable.find(item=>
            item.id == d.id
          );
          if(tempTable){

          }else{
            self.RomeData.queueTableData.splice(index, 1)
          }
        });


        var data ={};
        data.Message = 'Heartbeat';
        data.Params = {
          'time':'Date()'
        }
        socket.send(JSON.stringify(data));//发送数据到服务端
          
      };
      socket.onclose=function(e){
        PrintConsole("关闭TCP连接onclose",e);
      };
      if (socket.readyState == WebSocket.OPEN) socket.onopen();       
    },
  }
};
</script>

<style>
.MainCard{
  height: 750px;
}
.TopCard{
  height: 320px;
}
.DownCard{
  height: 390px;
}

</style>
