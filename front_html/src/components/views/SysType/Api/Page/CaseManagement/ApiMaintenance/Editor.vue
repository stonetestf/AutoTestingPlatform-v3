<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="1200px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :before-close="dialogClose">
                <el-steps :active="StepsRomeData.active" simple :process-status="StepsRomeData.processStatus" finish-status="success">
                    <el-step title="维护基本信息"></el-step>
                    <el-step title="编写接口信息"></el-step>
                    <el-step title="效验接口参数"></el-step>
                </el-steps>
                <el-card style="height:755px"
                    v-loading="loading"
                    element-loading-text="拼命加载中"
                    element-loading-spinner="el-icon-loading">
                    <template v-if="StepsRomeData.active==0">
                        <div class="table">
                            <div class="father" style="width: 100%; height: 550px;">
                                <div class="son" style="width:1100px; height: 150px;">
                                    <div style="margin-top:20px;">
                                        <el-card shadow="never">
                                            <el-form ref="BasicRomeData" :inline="true" :rules="BasicRomeData.rules" :model="BasicRomeData"  label-width="100px">
                                                <el-form-item label="所属页面:" prop="pageId">
                                                    <el-select v-model="BasicRomeData.pageId" clearable placeholder="请选择" @click.native="GetPageNameOption()">
                                                        <el-option
                                                            v-for="item in BasicRomeData.pageNameOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="所属功能:" prop="funId">
                                                    <el-select v-model="BasicRomeData.funId" clearable placeholder="请选择" @click.native="GetFunNameOption()">
                                                        <el-option
                                                            v-for="item in BasicRomeData.funNameOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="页面环境:" prop="environmentId">
                                                    <el-select v-model="BasicRomeData.environmentId" clearable placeholder="请选择" @click.native="GetPageEnvironmentNameOption()">
                                                        <el-option
                                                            v-for="item in BasicRomeData.environmentNameOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="接口名称:" prop="apiName">
                                                    <el-input placeholder="请输入接口名称" v-model="BasicRomeData.apiName" style="width:550px;"></el-input>
                                                </el-form-item>
                                                <el-form-item label="接口状态:" prop="apiState">
                                                    <el-select v-model="BasicRomeData.apiState" clearable placeholder="请选择" >
                                                        <el-option
                                                            v-for="item in BasicRomeData.apiStateOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                            </el-form>
                                        </el-card>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==1">
                        <el-form ref="EditApiRomeData" :model="EditApiRomeData" label-width="100px">
                            <el-form-item>
                                <el-input placeholder="请输入接口地址" style="margin-left:-90px;" v-model="EditApiRomeData.requestUrl">
                                    <el-select v-model="EditApiRomeData.requestType" slot="prepend" style="width:97px">
                                        <el-option
                                            v-for="item in EditApiRomeData.requestTypeOption"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-input>
                                <el-button type="primary" @click="SendRequest()">Send</el-button>
                            </el-form-item>
                            <el-tabs v-model="EditApiRomeData.activeName" @tab-click="handleClick" style="margin-top:-10px">
                                <el-tab-pane :label="EditApiRomeData.headersName" name="Headers">
                                    <el-table
                                        :data="EditApiRomeData.headersRomeData.tableData"
                                        border
                                        height="563">
                                        <el-table-column
                                            label="启用"
                                            width="70px"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="参数名"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.key" placeholder="Key"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="参数值"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.value" placeholder="Value"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="备注"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.remarks" placeholder="Remark"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            align="center"
                                            width="65px">
                                        <template slot="header">
                                            <el-button type="success" size="mini" icon="el-icon-circle-plus-outline" @click="CreateNewHeadersData()"></el-button>
                                        </template>
                                        <template slot-scope="scope" style="width:100px">
                                        <el-button
                                            size="mini"
                                            icon="el-icon-delete"
                                            type="danger"
                                            @click="handleHeadersDelete(scope.$index, scope.row)"></el-button>
                                        </template>
                                        </el-table-column>
                                    </el-table>
                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.paramsName" name="Params">
    
                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.bodyName" name="Body">

                                </el-tab-pane>
                                <el-tab-pane label="File" name="File">

                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.extractName" name="Extract">

                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.validateName" name="Validate">

                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.preOperationName" name="PreOperation">

                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.rearOperationName" name="RearOperation">

                                </el-tab-pane>
                            </el-tabs>
                        </el-form>
                    </template>
                    <template v-else>
                    </template>
                </el-card>
                <el-button style="margin-top: 12px;" icon="el-icon-arrow-left" type="primary" v-if="StepsRomeData.disPlay_Previous" @click="previous">上一步</el-button>
                <el-button style="margin-top: 12px;" type="primary" v-if="StepsRomeData.disPlay_Next" @click="next">下一步<i class="el-icon-arrow-right el-icon--right"></i></el-button>
                <el-button style="margin-top: 12px;" type="success" v-if="StepsRomeData.disPlay_Save" @click="returnToMain()">保存</el-button>
            </el-drawer>
        </template>
    </div>
</template>

<script>

import {PrintConsole} from "../../../../../../js/Logger.js";
import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetPageEnvironmentNameItems} from "../../../../../../js/GetSelectTable.js";

export default {
    components: {
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            StepsRomeData:{
                active:0,
                stepLength:2,//步长，整个窗口可以执行的步骤数
                processStatus:'process',
                disPlay_Save:false,
                disPlay_Next:true,
                disPlay_Previous:false,
            },
            BasicRomeData:{
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                environmentId:'',//页面环境
                environmentNameOption:[],
                apiName:'',
                apiState:'',
                apiStateOption:[
                    {'label':'启用','value':'0'},
                    {'label':'禁用','value':'1'},
                ],
                rules:{
                    pageId:[{ required: true, message: '请选择所属页面', trigger: 'change' }],
                    funId:[{ required: true, message: '请选择所属功能', trigger: 'change' }],
                    environmentId:[{ required: true, message: '请选择环境地址', trigger: 'change' }],
                    apiName:[
                        { required: true, message: '请输入接口名称', trigger: 'blur' },
                        { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
                    ],
                    apiState:[{ required: true, message: '请选择状态', trigger: 'change' }],
                },
            },
            EditApiRomeData:{
                requestUrl:'',
                requestType:'GET',
                requestTypeOption:[
                    {'label':'GET','value':'GET'},
                    {'label':'POST','value':'POST'},
                ],
                activeName:'Headers',
                headersName:'Headers',
                paramsName:'Params',
                bodyName:'Body',
                extractName:'Extract/提取',
                validateName:'Validate/断言',
                preOperationName:'前置操作',
                rearOperationName:'后置操作',
                headersRomeData:{
                    index:0,
                    tableData:[],
                },

            },
        };
    },
    mounted(){

    },
    computed:{//计算属性

    },
    props:[//main页面在引用editor时 必须声明所需要调用的属性
        'isVisible','dialogPara'
    ],
    watch:{//当我们输入值后，wacth监听每次修改变化的新值，然后计算输出值
        isVisible:{//用于监听父页面的isVisible，true时就弹出窗口
            handler(newval,oldval)
            {
                this.dialogVisible=newval;  
            }
        },
        dialogPara:{
            handler(newval,oldval)
            {
                PrintConsole(newval);
                this.ClearStepsRomeData();
                this.ClearBasicRomeData();
                this.ClearEditApiRomeData();
                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew

                if(newval.isAddNew==false){//进入编辑状态
                
                }
            }
        },
        'StepsRomeData.active': function (newVal,oldVal) {//监听步骤
            // console.log('newVal:'+newVal)
            let self = this;
            if(newVal==0){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = false;
               
            }else if(newVal==1){
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = true;
                self.StepsRomeData.disPlay_Save = false;
            }else{
                self.StepsRomeData.disPlay_Save = true;
                self.StepsRomeData.disPlay_Next = false;
                self.StepsRomeData.disPlay_Previous = true;
            }
            console.log('步骤',this.StepsRomeData.active)
        },
        'BasicRomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.BasicRomeData.funId='';
                self.BasicRomeData.funNameOption=[];
            }
        },
        'EditApiRomeData.headersRomeData.index': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditApiRomeData.headersRomeData.tableData.length;
                if(dataLength==0){
                    self.EditApiRomeData.headersName='Headers';
                }else{
                    self.EditApiRomeData.headersName='Headers('+dataLength+')';
                }
                
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        //导航条事件
        next() {//下一步
            let self = this;
            PrintConsole('当前',self.StepsRomeData.active)
            if(self.StepsRomeData.active==0){//基本用例数据
                self.StepsRomeData.active++;
                // this.$refs['BasicRomeData'].validate((valid) => {
                //     if (valid) {//通过
                //         self.StepsRomeData.active++;
                //     } 
                // });
            }else if(self.StepsRomeData.active==1){
                self.StepsRomeData.active++;
            }
        },
        previous(){//上一步
            let self = this;
            self.StepsRomeData.processStatus='process';
            if(self.StepsRomeData.active==0){

            }else if(self.StepsRomeData.active==3){
                self.StepsRomeData.active--;
                self.StepsRomeData.active--;
            }
            else{
                self.StepsRomeData.active--;
            }
            PrintConsole('步骤',this.StepsRomeData.active)
        },
        ClearStepsRomeData(){
            let self = this;
            // self.resetForm('RomeData');
            self.StepsRomeData.active= 0;
            self.StepsRomeData.disPlay_Save = false;
            self.StepsRomeData.disPlay_Next = true;
            self.StepsRomeData.processStatus ='process';
        },
        returnToMain(){
            let self = this;
            self.dialogVisible = false;//关闭新增弹窗
            self.$emit('closeDialog');
            self.$emit('Succeed');//回调查询   
        },

        //基本信息
        ClearBasicRomeData(){
            let self = this;
            self.resetForm('BasicRomeData');

        },
        GetPageNameOption(){
            GetPageNameItems(this.$cookies.get('proId')).then(d=>{
                this.BasicRomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            if(this.BasicRomeData.pageId){
                GetFunNameItems(this.$cookies.get('proId'),this.BasicRomeData.pageId).then(d=>{
                    this.BasicRomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        GetPageEnvironmentNameOption(){
            GetPageEnvironmentNameItems(this.$cookies.get('proId')).then(d=>{
                this.BasicRomeData.environmentNameOption = d;
            });
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                PrintConsole('清除正则验证')
                this.$refs[formName].resetFields();
            }
        },

        //编辑接口信息
        ClearEditApiRomeData(){
            let self = this;
            self.EditApiRomeData.requestType='GET';
            self.EditApiRomeData.activeName='Headers';
            self.EditApiRomeData.headersName='Headers';
            self.EditApiRomeData.paramsName='Params';
            self.EditApiRomeData.bodyName='Body';
            self.EditApiRomeData.extractName='Extract/提取';
            self.EditApiRomeData.validateName='Validate/断言';
            self.EditApiRomeData.preOperationName='前置操作';
            self.EditApiRomeData.rearOperationName='后置操作';

            //headersRomeData
            self.EditApiRomeData.headersRomeData.tableData=[];
            self.EditApiRomeData.headersRomeData.index=0;
        },
        handleClick(tab, event){
            PrintConsole(tab);
        },

        //headersRomeData
        CreateNewHeadersData(){
            let self = this;
            let obj = {};
            obj.index = self.EditApiRomeData.headersRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.value='';
            obj.remarks='';

            self.EditApiRomeData.headersRomeData.tableData.push(obj);
            self.EditApiRomeData.headersRomeData.index+=1;
        },
        handleHeadersDelete(index,row){
            PrintConsole('handleHeadersDelete',row);
            let self = this;
            self.EditApiRomeData.headersRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditApiRomeData.headersRomeData.tableData.forEach((item,i)=>{
                self.EditApiRomeData.headersRomeData.tableData[i].index = i;
            });

            self.EditApiRomeData.headersRomeData.index -=1 ;
        },
    }
};
</script>

<style>
.table {display: table; width: 100%;}
.father {display: table-cell; vertical-align: middle;}
.son {margin: auto;}
</style>
