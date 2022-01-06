<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="1200px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :close-on-press-escape="false"
            :before-close="dialogClose">
                <el-steps :active="StepsRomeData.active" simple :process-status="StepsRomeData.processStatus" finish-status="success">
                    <el-step title="维护基本信息"></el-step>
                    <el-step title="排列用例集"></el-step>
                    <el-step title="效验定时任务"></el-step>
                </el-steps>
                <el-card style="height:755px"
                    v-loading="loading"
                    element-loading-text="拼命加载中"
                    element-loading-spinner="el-icon-loading">
                    <template v-if="StepsRomeData.active==0">
                        <div class="table">
                           <div class="father" style="width: 100%; height: 600px;">
                                <div class="son" style="width: 1000px; height: 150px;">
                                    <el-card style="width:1000px" shadow="never">
                                        <el-form ref="BasicRomeData" :inline="true" :rules="BasicRomeData.rules" :model="BasicRomeData"  label-width="100px">
                                            <el-form-item label="任务名称:" prop="taskName" >
                                                <el-input v-model.trim="BasicRomeData.taskName" clearable style="width:515px;"></el-input>
                                            </el-form-item>
                                            <el-form-item label="页面环境:" prop="environmentId">
                                                <el-select v-model="BasicRomeData.environmentId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetPageEnvironmentNameOption()">
                                                    <el-option
                                                        v-for="item in BasicRomeData.environmentNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item label="定时配置:" prop="timingConfig" >
                                                <el-input v-model="BasicRomeData.timingConfig" style="width:200px;float:left;"></el-input>
                                            </el-form-item>
                                            <el-form-item label="优先级:" prop="priorityId">
                                                <el-select v-model="BasicRomeData.priorityId" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.priorityNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                        <span style="float: left">{{ item.label }}</span>
                                                        <span style="float: right; color: #8492a6; font-size: 13px">{{ item.details }}</span>
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item label="任务状态:" prop="taskStatus">
                                                <el-select v-model="BasicRomeData.taskStatus" clearable placeholder="请选择"  style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.taskStatusOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <div style="margin-left:-313px">
                                                <el-form-item label="关联用户:">
                                                    <el-cascader 
                                                        @click.native="GetUserNameOption()"
                                                        style="width:515px"
                                                        v-model="BasicRomeData.pushTo" 
                                                        :options="BasicRomeData.userNameOptions" 
                                                        :props="BasicRomeData.props" 
                                                        :show-all-levels="false" 
                                                        clearable
                                                        placeholder="被关联者会收到任务运行完成后的邮件提醒">
                                                        <template slot-scope="{ node, data }">
                                                            <span>{{ data.label }}</span>
                                                            <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                                        </template>
                                                    </el-cascader>
                                                </el-form-item>
                                            </div>
                                        </el-form>
                                    </el-card>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==1">
                        <el-table
                            id="TestSet" 
                            row-key="id"
                            :data="SortCaseRomeData.tableData"
                            height="710px"
                            border>
                            <el-table-column
                                label="步骤"
                                align= "center"
                                type="index"
                                width="80">
                            </el-table-column>
                            <el-table-column
                                label="测试类型"
                                align= "center"
                                width="100px">
                                <template slot-scope="scope">
                                    <el-tag type="info" v-if="scope.row.testType=='UnitTest'" >单元测试</el-tag>
                                    <el-tag type="warning" v-else-if="scope.row.testType=='HybridTest'" >混合测试</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="用例名称"
                                align= "center"
                                width="350px"
                                prop="caseName">
                            </el-table-column>
                            <el-table-column
                                label="所属页面"
                                align= "center"
                                prop="pageName">
                            </el-table-column>
                            <el-table-column
                                label="所属功能"
                                align= "center"
                                prop="funName">
                            </el-table-column>
                            <el-table-column
                                label="用例状态"
                                align= "center"
                                width="100px">
                                <template slot-scope="scope">
                                    <el-tag type="warning" v-if="scope.row.caseState=='InDev'">研发中</el-tag>
                                    <el-tag type="success" v-else-if="scope.row.caseState=='Completed'">已完成</el-tag>
                                    <!-- <el-tag type="success" v-else-if="scope.row.caseState=='Completed'"><i class="el-icon-check"></i></el-tag> -->
                                    <el-tag type="info" v-else>弃用</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="启用"
                                align= "center"
                                width="90px">
                                <template slot-scope="scope">
                                <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                </template>
                            </el-table-column>
                            <el-table-column
                                align="center"
                                width="100px">
                                <template slot="header">
                                    <el-button type="primary" @click="OpenCaseMainDialog()">新增</el-button>
                                </template>
                                <template slot-scope="scope" style="width:100px">
                                    <el-button
                                        size="mini"
                                        type="danger"
                                        @click="handleDelete(scope.$index, scope.row)">移除
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </template>
                    <template v-else>
                        <div slot="header">
                            {{CharmRomeData.title}}
                        </div>
                        <div>
                            <el-table
                            :data="CharmRomeData.tableData"
                            border
                            height="660px">
                            <el-table-column
                                type="index"
                                align= "center"
                                label="Index"
                                width="100">
                            </el-table-column>
                            <el-table-column
                                prop="stepsName"
                                align= "center"
                                label="错误步骤"
                                width="200">
                            </el-table-column>
                            <el-table-column
                                prop="errorMsg"
                                align= "center"
                                label="错误信息">
                            </el-table-column>
                            <el-table-column
                                prop="updateTime"
                                align= "center"
                                label="错误时间"
                                width="200">
                            </el-table-column>
                            </el-table>
                        </div>
                    </template>
                </el-card>
                <el-button style="margin-top: 12px;" icon="el-icon-arrow-left" type="primary" v-if="StepsRomeData.disPlay_Previous" @click="previous">上一步</el-button>
                <el-button style="margin-top: 12px;" type="primary" v-if="StepsRomeData.disPlay_Next" @click="next">下一步<i class="el-icon-arrow-right el-icon--right"></i></el-button>
                <el-button style="margin-top: 12px;" type="success" v-if="StepsRomeData.disPlay_Save" @click="SaveData()">保存</el-button>
            </el-drawer>
        </template>
        <template>
            <dialog-case-main
                @closeDialog="CloseCaseMainDialog" 
                :isVisible="dialog.caseMain.dialogVisible" 
                :dialogPara="dialog.caseMain.dialogPara"
                @getData="AddToTestSetTable($event)">
            </dialog-case-main>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import Sortable from 'sortablejs';
import {PrintConsole} from "../../../../../../js/Logger.js";

import {GetPageEnvironmentNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetUserNameItems} from "../../../../../../js/GetSelectTable.js";
import DialogCaseMain from "./CaseMain.vue";

export default {
    components: {
        DialogCaseMain
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            StepsRomeData:{
                active:0,
                stepLength:3,//步长，整个窗口可以执行的步骤数
                processStatus:'process',
                disPlay_Save:false,
                disPlay_Next:true,
                disPlay_Previous:false,
            },
            BasicRomeData:{
                taskName:'',
                environmentId:'',
                environmentNameOption:[],
                timingConfig:'',
                priorityId:'',//优先级
                priorityNameOption:[
                    {'label':'P0','value':'P0','details':'最高'},
                    {'label':'P1','value':'P1','details':'高'},
                    {'label':'P2','value':'P2','details':'中'},
                    {'label':'P3','value':'P3','details':'低'},
                ],
                taskStatus:'',
                taskStatusOption:[
                    {'label':'开启','value':1},
                    {'label':'关闭','value':0},
                ],
                props: { multiple: true },
                pushTo:[],
                userNameOptions:[],
                rules:{
                    taskName: [
                        { required: true, message: '请输入任务名称', trigger: 'blur' },
                        { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                    ],
                    environmentId:[{required: true, message: '请选择页面环境', trigger: 'change' }],
                    timingConfig: [
                        { required: true, message: '请输入正确的CronTab时间', trigger: 'blur' },
                        { min: 1, max: 10, message: '例:* * * * *', trigger: 'blur' }
                    ],
                    priorityId:[{required: true, message: '请选择优先级', trigger: 'change' }],
                    taskStatus:[{required: true, message: '请选择任务状态', trigger: 'change' }],
                    
                },

            },
            SortCaseRomeData:{
                tableData:[]
            },
            CharmRomeData:{
                title:'',
                tableData:[],
            },
            dialog:{
                caseMain:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
            }
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
                this.ClearSortCaseRomeData();

                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew;

                if(newval.isAddNew==false){//进入编辑状态
                  
                }
            }
        },
        'StepsRomeData.active': function (newVal,oldVal) {//监听所属项目有变化
            // console.log('newVal:'+newVal)
            let self = this;
            if(newVal==0){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = false;
            }else if(newVal==1){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Previous = true;
                self.StepsRomeData.disPlay_Next = true;
            }else{
                self.StepsRomeData.disPlay_Save = true;
                self.StepsRomeData.disPlay_Next = false;
                self.StepsRomeData.disPlay_Previous = true;
                
            }
            PrintConsole('步骤',this.StepsRomeData.active)
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        //导航条事件
        next() {//下一步
            let self = this;
            if(self.StepsRomeData.active==0){//基本用例数据
                self.StepsRomeData.active++;
                self.$nextTick(function () {//当DOM加载完成后才会执行这个!
                    self.rowDrop();
                });
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

            }
            else{
                self.StepsRomeData.active--;
            }
            // PrintConsole('步骤',self.StepsRomeData.active)
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

        //基础信息
        ClearBasicRomeData(){
            let self = this;
            self.resetForm('BasicRomeData');
            self.BasicRomeData.taskName='';
            self.BasicRomeData.environmentId='';
            self.BasicRomeData.timingConfig='';
            self.BasicRomeData.priorityId='';
            self.BasicRomeData.taskStatus='';
            self.BasicRomeData.pushTo='';
        },
        GetPageEnvironmentNameOption(){
            GetPageEnvironmentNameItems(this.$cookies.get('proId')).then(d=>{
                this.BasicRomeData.environmentNameOption = d;
            });
        },
        GetUserNameOption(){
            GetUserNameItems().then(d=>{
                this.BasicRomeData.userNameOptions = d;
            });
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },

        //用例集
        ClearSortCaseRomeData(){
            let self = this;
            self.SortCaseRomeData.tableData=[];
        },
        CloseCaseMainDialog(){
            this.dialog.caseMain.dialogVisible = false;
        },
        OpenCaseMainDialog(){
            let self = this;
            let passCaseId = [];
            self.SortCaseRomeData.tableData.forEach(d=>{
                passCaseId.push(d.id)
            });
                
            self.dialog.caseMain.dialogPara={
                dialogTitle:"导入用例",//初始化标题
                passCaseId:passCaseId
            }
            self.dialog.caseMain.dialogVisible=true;
        },
        AddToTestSetTable(data){
            let self = this;
            PrintConsole('回调数据:',data);
            data.forEach(d=>{
                let obj = {};
                obj.id=d.id;
                obj.testType=d.testType;
                obj.pageName = d.pageName;
                obj.funName = d.funName;
                obj.caseName = d.caseName;
                obj.caseState = d.caseState;
                obj.state = true;

                self.SortCaseRomeData.tableData.push(obj);
            });
            self.rowDrop();
            PrintConsole('列表保存数据:',self.SortCaseRomeData.tableData);   
        },
        handleDelete(index,row){
            let self = this;
            this.$confirm('请确定是否移除此条数据?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                    self.SortCaseRomeData.tableData.splice(index,1);
                    PrintConsole('最终数据:',self.SortCaseRomeData.tableData);
                }).catch(() => {       
            });
        },
        rowDrop() {//排序方法
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#TestSet > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.SortCaseRomeData.tableData.splice(oldIndex, 1)[0];
                    self.SortCaseRomeData.tableData.splice(newIndex, 0, currRow);
                    // console.log(self.RomeData.TableData);
                }
            });
        },
    }
};
</script>

<style>
.table {display: table; width: 100%;}
.father {display: table-cell; vertical-align: middle;}
.son {margin: auto;}
.bodyRome{
    margin-top:10px;
}
</style>
