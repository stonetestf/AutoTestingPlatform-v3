<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div style="">
                <el-row>
                    <el-col :span="2">
                        <el-menu
                            default-active="2"
                            class="MainMenu"
                            @select="handleSelect"
                            @open="handleOpen"
                            @close="handleClose"
                            background-color="#545c64"
                            text-color="#fff"
                            active-text-color="#ffd04b">
                            <el-menu-item index="0">
                                <i class="el-icon-menu"></i>
                                <span slot="title">总览</span>
                            </el-menu-item>
                            <el-menu-item index="1">
                                <i class="el-icon-receiving"></i>
                                <span slot="title">套件</span>
                            </el-menu-item>
                            <el-menu-item index="2">
                                <i class="el-icon-document"></i>
                                <span slot="title">日志</span>
                            </el-menu-item>
                            <!-- <el-menu-item></el-menu-item>
                            <el-menu-item></el-menu-item>
                            <el-menu-item></el-menu-item>
                            <el-menu-item index="10" v-if="isCollapse">
                                <i class="el-icon-arrow-right"></i>
                                <span slot="title">展开</span>
                            </el-menu-item>
                            <el-menu-item index="11" v-else>
                                <i class="el-icon-arrow-left"></i>
                                <span slot="title">折叠</span>
                            </el-menu-item> -->
                        </el-menu>
                    </el-col>
                    <el-col :span="21">
                        <el-card class="MainCard" v-show="OverviewRomeData.disPlay">
                            <div>
                                <el-row :gutter="20">
                                    <el-col :span="11">
                                        <el-card shadow="never" style="height:300px">
                                            <el-row>
                                                <el-col :span='24'>
                                                    <h2 style="margin-top:-10px;float:left">{{OverviewRomeData.titleClass.reportName}}</h2>
                                                    <div style="margin-top:-10px;margin-left:10px;float:left">
                                                        <el-tag v-if="OverviewRomeData.titleClass.reportStatus=='Pass'" type="success">通过</el-tag>
                                                        <el-tag v-else type="warning">未通过</el-tag>
                                                    </div>
                                                </el-col>
                                            </el-row>
                                            <el-row>
                                                <el-col :span='24'>
                                                    <div style="float:left">
                                                        <span><b>创建时间:</b>{{OverviewRomeData.titleClass.createTime}}</span>
                                                    </div>
                                                </el-col>
                                            </el-row>
                                            <el-row>
                                                <el-col :span='24'>
                                                    <div style="float:left;margin-top:5px">
                                                        <span><b>耗时时长:</b>{{OverviewRomeData.titleClass.runningTime}} ms</span>
                                                    </div>
                                                </el-col>
                                            </el-row>
                                            <el-row>
                                                <el-col :span='24'>
                                                    <div style="float:left;margin-top:5px">
                                                        <span><b>创建人:</b>{{OverviewRomeData.titleClass.createUserName}}</span>
                                                    </div>
                                                </el-col>
                                            </el-row>
                                            <el-row>
                                                <el-col :span='12'>
                                                    <div style="margin:10px 0px 0px 60px">
                                                        <el-row>
                                                            <el-col :span='24'>
                                                                <div>
                                                                    <h1>{{OverviewRomeData.titleClass.total}}</h1>
                                                                </div>
                                                            </el-col>
                                                        </el-row>
                                                        <el-row>
                                                            <el-col :span='24'>
                                                                <div style="margin-top:-20px">
                                                                    <span v-if="RomeData.reportType=='API'">独立接口</span>
                                                                    <span v-else-if="RomeData.reportType=='CASE'">独立接口</span>
                                                                    <span v-else-if="RomeData.reportType=='TASK'">测试用例</span>
                                                                    <span v-else-if="RomeData.reportType=='BATCH'">定时任务</span>
                                                                </div>
                                                            </el-col>
                                                        </el-row>
                                                    </div>
                                                </el-col>
                                                <el-col :span='12'>
                                                    <!-- <el-card> -->
                                                    <!-- </el-card> -->
                                                    <div style="margin-top:-130px;margin-left:-120px;" id="EchartContainer-pie" class="EchartContainer-pie"></div>   
                                                </el-col>
                                            </el-row>
                                        </el-card>
                                    </el-col>
                                    <el-col :span="13">
                                        <el-card shadow="never" style="height:300px;width:910px">
                                            <div style="margin-top:-10px" id="EchartContainer-trend" class="EchartContainer-trend"></div>   
                                        </el-card>
                                    </el-col>
                                </el-row>
                            </div>
                            <div style="margin-top:20px">
                                <el-row :gutter="20">
                                    <el-col :span="11">
                                        <el-card shadow="never" style="height:570px">
                                            <div slot="header" style="text-align: left;">
                                                <span v-if="RomeData.reportType=='API'">独立接口</span>
                                                <span v-else-if="RomeData.reportType=='CASE'">独立接口</span>
                                                <span v-else-if="RomeData.reportType=='TASK'">测试用例</span>
                                                <span v-else-if="RomeData.reportType=='BATCH'">定时任务</span>
                                                <span style="color: darkgray;">总共{{OverviewRomeData.dataTable.length}}项</span>
                                            </div>
                                            <div>
                                                <el-table
                                                    style="margin-top:-20px"
                                                    :data="OverviewRomeData.dataTable"
                                                    height="513px">
                                                    <el-table-column
                                                        label="ID"
                                                        align= "center"
                                                        width="70px"
                                                        prop="id">
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="名称"
                                                        align= "center"
                                                        prop="name">
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="统计"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-tag type="success">Pass:{{scope.row.passTotal}}</el-tag>
                                                            <el-tag type="warning">Fail:{{scope.row.failTotal}}</el-tag>
                                                            <el-tag type="danger">Error:{{scope.row.errorTotal}}</el-tag>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="通过率"
                                                        width="80px"
                                                        align= "center"
                                                        prop="passRate">
                                                    </el-table-column>
                                                </el-table>
                                            </div>
                                        </el-card>
                                    </el-col>
                                    <el-col :span="13">
                                        <div>
                                            <el-card shadow="never" style="height:570px">
                                                <div slot="header" style="text-align: left;">
                                                    <span>警示信息</span>
                                                    <span style="color: darkgray;">总共{{OverviewRomeData.warningDataTable.length}}项</span>
                                                </div>
                                                <div>
                                                    <el-table
                                                        style="margin-top:-20px"
                                                        :data="OverviewRomeData.warningDataTable"
                                                        height="513px">
                                                        <el-table-column
                                                            label="ID"
                                                            align= "center"
                                                            width="70px"
                                                            prop="id">
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="触发类型"
                                                            width="100px"
                                                            align= "center">
                                                            <template slot-scope="scope">
                                                                <el-tag type="warning" v-if="scope.row.triggerType=='Fail'">Fail</el-tag>
                                                                <el-tag type="danger" v-else-if="scope.row.triggerType=='Error'">Error</el-tag>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="名称"
                                                            width="300px"
                                                            align= "center"
                                                            prop="name">
                                                        </el-table-column>
                                                        <el-table-column
                                                            show-overflow-tooltip
                                                            label="信息"
                                                            align= "center"
                                                            prop="info">
                                                        </el-table-column>
                                                    </el-table>
                                                </div>
                                            </el-card>
                                        </div>
                                    </el-col>
                                </el-row>
                            </div>
                        </el-card>
                        <el-card class="MainCard" v-show="SuiteRomeData.disPlay">
                            <el-row :gutter="5">
                                <el-col :span="10">
                                    <el-card shadow="never" style="height:890px">
                                        <div>
                                            <el-button-group>
                                                <el-button type="info" @click="AllShrink()">概要&nbsp;{{OverviewRomeData.titleClass.passRate}}%</el-button>
                                                <el-button type="danger" @click="SelectCase('error')">错误&nbsp;{{OverviewRomeData.titleClass.errorTotal}}</el-button>
                                                <el-button type="warning">失败&nbsp;{{OverviewRomeData.titleClass.failTotal}}</el-button>
                                                <el-button type="success">成功&nbsp;{{OverviewRomeData.titleClass.passTotal}}</el-button>
                                                <el-button type="primary" @click="AllExpand()">所有&nbsp;{{OverviewRomeData.titleClass.allTotal}}</el-button>
                                            </el-button-group>
                                        </div>
                                        <div style="margin-top:10px">
                                            <el-input
                                                placeholder="输入关键字进行过滤"
                                                v-model="SuiteRomeData.leftRomeData.filterText">
                                            </el-input>
                                            <el-tree 
                                                :data="SuiteRomeData.leftRomeData.tableData" 
                                                :props="SuiteRomeData.leftRomeData.defaultProps">
                                                <span class="custom-tree-node" slot-scope="{ node }">
                                                    <span>{{ node.label }}</span>
                                                

                                                    <span style="margin-left:200px">
                                                        <el-tag type="success" size="mini">1</el-tag>
                                                        <el-tag type="warning" size="mini">2</el-tag>
                                                        <el-tag type="danger" size="mini">3</el-tag>
                                                    </span>
                                                </span>
                                            </el-tree>
                                        </div>
                                    </el-card>
                                </el-col>
                                <el-col :span="14">
                                    <el-card shadow="never" style="height:890px">
                                    </el-card>
                                </el-col>
                            </el-row>
                        </el-card>
                    </el-col>
                </el-row>
            </div>
        </template>
    </div>
</template>

<script>
import * as echarts from 'echarts';
import {PrintConsole} from "../../../../../js/Logger.js";
export default {
    data() {
        return {
            loading:false,
            // isCollapse: true,
            RomeData:{
                testReportId:'',
                reportType:'API',
            },
            OverviewRomeData:{//总览
                disPlay:true,
                //标题类
                titleClass:{
                    reportName:'测试接口报告',
                    reportStatus:'Pass',
                    createTime:'2020-01-01 12:22:33',
                    runningTime:'20',
                    total:'100',
                    createUserName:'lipenglo',
                    passTotal:1,
                    failTotal:2,
                    errorTotal:3,
                    allTotal:10,
                    passRate:'33',
                },
                trendChart:{//趋势图
                    reportIdList:['#1', '#12', '#33', '#34', '#35', '#36', '#40'],
                    passList:[120, 132, 101, 134, 90, 230, 210],
                    failList:[220, 182, 191, 234, 290, 330, 310],
                    errorList:[150, 232, 201, 154, 190, 330, 410],
                },
                dataTable:[
                    {'id':1,'name':'测试登录接口','passTotal':1,'failTotal':2,'errorTotal':3,'passRate':'30%'},
                ],//当前接口，用例，定时任务，批量任务的简要列表
                warningDataTable:[
                    {'id':1,'triggerType':'Fail','name':'测试登录接口','info':'我警告你','updateTime':'2020-22-11 12:22:32'},
                    {'id':1,'triggerType':'Error','name':'测试登录接口','info':'我出错误了你大爷的','updateTime':'2020-22-11 12:22:32'},
                ],
            },
            SuiteRomeData:{//套件
                disPlay:false,
                leftRomeData:{
                    filterText:'',
                    tableData:[
                        {label: '测试定时任务',id:'1',layerType:'TASK',children: [
                            {label: '测试登录',id:'1',layerType:'CASE',children: 
                            [
                                {label: '登录',layerType:'API',id:'1',reportStatus:'Pass'},
                                {label: '查询',layerType:'API',id:'2',reportStatus:'Fail'},
                            ]}
                        ]}, 
                    ],
                    defaultProps:{
                        children: 'children',
                        label: 'label'
                    }
                }
                

            }
        };
    },
    mounted(){
        PrintConsole('query',this.$route.query);
        // this.RomeData.testReportId = this.$route.query.testReportId;
        // this.RomeData.reportType = this.$route.query.reportType;

        this.PieChart(this.OverviewRomeData.titleClass.passRate);
        this.TrendChart();

    },
    methods: {
        handleOpen(key, keyPath) {
            PrintConsole(key, keyPath);
        },
        handleClose(key, keyPath) {
            PrintConsole(key, keyPath);
        },
        handleSelect(key, keyPath){
            PrintConsole(key, keyPath);
            if(key=='0'){
                this.OverviewRomeData.disPlay=true;
                this.SuiteRomeData.disPlay=false;
            }else if(key=='1'){
              this.SuiteRomeData.disPlay=true;
              this.OverviewRomeData.disPlay=false;
            }
        },



        PieChart(passRate){//通过率
            let self = this;
            var MyChart_pie = echarts.init(document.getElementById('EchartContainer-pie'));//初始化
            var option = {//设置各属性和数据
                tooltip: {
                    trigger: 'item', //通过哪种方式触发tip
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                series:[{
                        name: '测试统计',
                        type: 'pie',
                        radius: ['40%', '70%'],
                        center: ['50%', '60%'],//好像是位置
                        label:{//中间文字配置
                            normal:{
                                show:true,
                                position:'center',
                                // color:'#9A9EBA',
                                fontSize:'17px',
                                formatter:'通过率\n'+passRate+'%',
                                emphasis:{//中间文字显示
                                    show:true
                                }
                            }
                        },
                        data:[
                            {"value": self.OverviewRomeData.titleClass.passTotal, "name": 'Pass', "itemStyle": {"normal": {"color": '#91cc75'}}},
                            {"value": self.OverviewRomeData.titleClass.failTotal, "name": 'Fail', "itemStyle": {"normal": {"color": '#fac858'}}},
                            {"value": self.OverviewRomeData.titleClass.errorTotal, "name": 'Error', "itemStyle": {"normal": {"color": '#ee6666'}}},
                        ],
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }] 
            };
            MyChart_pie.setOption(option,true);//加载属性后显示 true自动每次清除数据
        },
        TrendChart(){//趋势图
            let self = this;
            var MyChart_trend = echarts.init(document.getElementById('EchartContainer-trend'));//初始化
            var option = {
                title: {
                    text: '历史趋势图'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        label: {
                            backgroundColor: '#6a7985'
                        }
                    }
                },
                // legend: {
                //     data: ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
                // },
                // toolbox: {
                //     feature: {
                //     saveAsImage: {}
                //     }
                // },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        data: self.OverviewRomeData.trendChart.reportIdList
                    }
                ],
                yAxis: [
                    {
                    type: 'value'
                    }
                ],
                series: [
                    {
                        name: 'Pass',
                        type: 'line',
                        stack: 'Total',
                        color: '#91cc75',
                        areaStyle: {},
                        emphasis: {
                            focus: 'series'
                        },
                        data: self.OverviewRomeData.trendChart.passList
                    },
                    {
                        name: 'Fail',
                        type: 'line',
                        stack: 'Total',
                        color: '#fac858',
                        areaStyle: {},
                        emphasis: {
                            focus: 'series'
                        },
                        data: self.OverviewRomeData.trendChart.failList
                    },
                    {
                        name: 'Error',
                        type: 'line',
                        color: '#ee6666',
                        stack: 'Total',
                        areaStyle: {},
                        emphasis: {
                            focus: 'series'
                        },
                        data: self.OverviewRomeData.trendChart.errorList
                    },
                ]
            };


            MyChart_trend.setOption(option,true);//加载属性后显示 true自动每次清除数据
        },
    }
};
</script>

<style>
.MainMenu{
    height: 930px;
}
.MainCard{
    height: 928px;
    width: 1740px;
}

.EchartContainer-pie{
    width:600px; 
    height:270px;
    
}

.EchartContainer-trend{
    width:900px; 
    height:280px;
    /* color: darkgray; */
}
</style>