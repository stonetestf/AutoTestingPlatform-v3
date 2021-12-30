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
                <el-steps :active="StepsRomeData.active" simple :process-status="StepsRomeData.processStatus" finish-status="success" >
                    <el-step title="上传JSON文件"></el-step>
                    <el-step title="解析JSON文件"></el-step>
                </el-steps>
                <el-card style="height:755px">
                    <template v-if="StepsRomeData.active==0">
                        <div>
                            <div style="margin:180px 0 0 330px">
                                <el-upload
                                    style="width:500px"
                                    drag
                                    multiple
                                    :headers="headers"
                                    :action="RomeData.uploadToTemp"
                                    :on-success="upload_success"
                                    :on-remove="upload_remove"
                                    :limit="1"
                                    :file-list="RomeData.fileList">
                                    <i class="el-icon-upload"></i>
                                    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                                    <div class="el-upload__tip" slot="tip">只能上传Json格式的文件</div>
                                </el-upload>
                            </div>
                            <div style="margin-top:60px">
                                <el-form :inline="true" ref="RomeData" :rules="RomeData.rules" :model="RomeData" method="post">
                                    <el-form-item label="所属页面:" prop="pageId">
                                        <el-select v-model="RomeData.pageId" clearable placeholder="请选择需要导入到的页面" style="width:200px;" @click.native="GetPageNameOption()">
                                            <el-option
                                                v-for="item in RomeData.pageNameOption"
                                                :key="item.value"
                                                :label="item.label"
                                                :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </el-form-item>
                                    <el-form-item label="所属功能:" prop="funId">
                                        <el-select v-model="RomeData.funId" clearable placeholder="请选择需要导入到位置" style="width:200px;" @click.native="GetFunNameOption()">
                                            <el-option
                                                v-for="item in RomeData.funNameOption"
                                                :key="item.value"
                                                :label="item.label"
                                                :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </el-form-item>
                                </el-form>
                            </div>
                        </div>
                    </template>
                    <template v-else>
                        <div
                        v-loading="loading"
                        element-loading-text="拼命加载中"
                        element-loading-spinner="el-icon-loading">
                            <div slot="header">
                                {{RomeData.title}}
                            </div>
                            <div>
                                <el-table
                                    :data=RomeData.tableData
                                    height="720px"
                                    border>
                                    <el-table-column
                                        label="接口名称"
                                        align= "center"
                                        width="300px"
                                        prop="apiName">
                                    </el-table-column>
                                    <el-table-column
                                        label="接口地址"
                                        align= "center"
                                        prop="requestUrl">
                                    </el-table-column>
                                    <el-table-column
                                        label="接口类型"
                                        width="100px"
                                        align= "center">
                                        <template slot-scope="scope">
                                            <el-tag type="success" v-if="scope.row.requestType=='GET'" >GET</el-tag>
                                            <el-tag type="warning" v-else-if="scope.row.requestType=='POST'">POST</el-tag>
                                            <el-tag type="info" v-else>{{scope.row.requestType}}</el-tag>
                                        </template>
                                    </el-table-column>    
                                    <el-table-column
                                        label="请求类型"
                                        width="120px"
                                        align= "center">
                                        <template slot-scope="scope">
                                            <el-tag type="infi">{{scope.row.requestParamsType}}</el-tag>
                                        </template>
                                    </el-table-column>
                                    <el-table-column
                                        label="参数样式"
                                        width="180px"
                                        align= "center"
                                        prop="bodyRequestType">
                                    </el-table-column>
                                    <el-table-column
                                        label="操作"
                                        align="center"
                                        width="100px">
                                    <template slot-scope="scope" style="width:100px">
                                        <el-button
                                            size="mini"
                                            type="danger"
                                            @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
                                    </template>
                                    </el-table-column>
                                </el-table>
                            </div>
                        </div>
                    </template>
                </el-card>
                <el-button style="margin-top: 12px;" icon="el-icon-arrow-left" type="primary" v-if="StepsRomeData.disPlay_Previous" @click="previous">上一步</el-button>
                <el-button style="margin-top: 12px;" type="primary" v-if="StepsRomeData.disPlay_Next" @click="next">下一步<i class="el-icon-arrow-right el-icon--right"></i></el-button>
                <el-button style="margin-top: 12px;" type="success" v-if="StepsRomeData.disPlay_Save" @click="DataSave()">保存</el-button>
            </el-drawer>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import store from '../../../../../../../store/index';
import {PrintConsole} from "../../../../../../js/Logger.js";

import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";


export default {
    components: {
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            // isAddNew:true,//是否是新增窗口
            loading:false,
            
            StepsRomeData:{
                active:0,
                stepLength:1,//步长，整个窗口可以执行的步骤数
                processStatus:'process',
                disPlay_Save:false,
                disPlay_Next:true,
                disPlay_Previous:false,
            },
            RomeData:{
                title:'',
                tableData:[],
                uploadToTemp:store.state.BackService +'/api/upLoad/UpLoadToTempPath',
                fileList:[],
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                rules: {
                    pageId:[{required: true, message: '请选择所属页面', trigger: 'change' }],
                    funId:[{required: true, message: '请选择所属功能', trigger: 'change' }],
                }
            },
        };
    },
    mounted(){

    },
    computed:{//计算属性
        headers(){//用来把token放到头部
            return {
                'Token': this.$cookies.get('token')
            }
        },
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
                this.ClearRomeData();

                this.dialogTitle = newval.dialogTitle;

         
            }
        },
        'StepsRomeData.active': function (newVal,oldVal) {//监听步骤
            // console.log('newVal:'+newVal)
            let self = this;
            if(newVal==0){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = false;
               
            }else{
                self.StepsRomeData.disPlay_Save = true;
                self.StepsRomeData.disPlay_Next = false;
                self.StepsRomeData.disPlay_Previous = true;
            }
            console.log('步骤',this.StepsRomeData.active)
        },
        'RomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.RomeData.funId='';
                self.RomeData.funNameOption=[];
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
            // self.StepsRomeData.active++;
            if(self.RomeData.fileList.length==0){
                self.$message.warning('请先上传Swagger的JSON格式文件!');
            }else{
                this.$refs['RomeData'].validate((valid) => {
                    if (valid) {//通过
                        self.StepsRomeData.active++;
                        self.analysisJsonData();
                    } 
                });
            }
        },
        previous(){//上一步
            let self = this;
            self.StepsRomeData.processStatus='process';
            if(self.StepsRomeData.active==0){

            }else{
                self.StepsRomeData.active--;
            }
            PrintConsole('步骤',this.StepsRomeData.active)
        },
        ClearStepsRomeData(){
            let self = this;
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

        //上传JSON
        ClearRomeData(){
            let self = this;
            self.resetForm('RomeData');
            self.RomeData.fileList=[];
            self.RomeData.pageId='';
            self.RomeData.funId='';
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        upload_success(response, file, fileList){
            let self = this;
            //这里的url地址要是网络地址，不然页面上只会加载一个白的图片
            self.RomeData.fileList.push({
                'name':response['file']['fileName'],
                'url':store.state.nginxUrl+'Temp/'+response['file']['fileName']}
            );
          
        },
        upload_remove(file, fileList){
            let self = this;
            PrintConsole(file);
            // self.RomeData.deleteFileList.push({'name':file.name,'url':file.url});
            self.RomeData.fileList=[];
        },
        GetPageNameOption(){
            GetPageNameItems(this.$cookies.get('proId')).then(d=>{
                this.RomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            if(this.RomeData.pageId){
                GetFunNameItems(this.$cookies.get('proId'),this.RomeData.pageId).then(d=>{
                    this.RomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        //解析JSON
        analysisJsonData(){
            let self = this;
            self.RomeData.tableData = [];
            self.loading=true;
            self.$axios.post('/api/ApiIntMaintenance/AnalysisJsonData',{
                'file':self.RomeData.fileList,
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.RomeData.tableData = res.data.dataTable;
                    self.loading=false;
                }
                else{
                    self.$message.error('文件解析失败:'+res.data.errorMsg);
                    self.loading=false;
                    self.StepsRomeData.active--;
                }
            }).catch(function (error) {
                console.log(error);
                // self.$message.error('文件解析失败:'+error);
                self.loading=false;
                self.StepsRomeData.active--;
            })
        },

    }
};
</script>

<style>

</style>
