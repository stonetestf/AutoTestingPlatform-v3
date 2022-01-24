<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="1920px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :close-on-press-escape="false"
            :before-close="dialogClose">
                <el-steps :active="StepsRomeData.active" simple :process-status="StepsRomeData.processStatus" finish-status="success">
                    <el-step title="维护基本信息"></el-step>
                    <el-step title="编写测试集"></el-step>
                    <el-step title="编写操作集"></el-step>
                    <el-step title="效验用例参数"></el-step>
                </el-steps>
                <el-card style="height:755px"
                    v-loading="loading"
                    element-loading-text="拼命加载中"
                    element-loading-spinner="el-icon-loading">
                    <template v-if="StepsRomeData.active==0">
                        <div class="table">
                            <div class="father" style="width: 100%; height: 650px;">
                                <div class="son" style="width: 950px; height: 200px;">
                                    <!-- <el-card style="width:1000px" shadow="never"> -->
                                    <div style="width:1000px">
                                        <el-form ref="BasicRomeData" :inline="true" :rules="BasicRomeData.rules" :model="BasicRomeData"  label-width="100px">
                                            <el-form-item prop="pageId" label="所属页面:">
                                                <el-select v-model="BasicRomeData.pageId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetPageNameOption()">
                                                    <el-option
                                                        v-for="item in BasicRomeData.pageNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="funId" label="所属功能:">
                                                <el-select v-model="BasicRomeData.funId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetFunNameOption()">
                                                    <el-option
                                                        v-for="item in BasicRomeData.funNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="environmentId" label="页面环境:">
                                                <el-select v-model="BasicRomeData.environmentId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetPageEnvironmentNameOption()">
                                                    <el-option
                                                        v-for="item in BasicRomeData.environmentNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="testType" label="测试类型:">
                                                <el-select v-model="BasicRomeData.testType" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.testTypeOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="labelId" label="用例标签:">
                                                <el-select v-model="BasicRomeData.labelId" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.labelNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="priorityId" label="优先级:">
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
                                            <el-form-item prop="caseName" label="用例名称:">
                                                <el-input v-model.trim="BasicRomeData.caseName" style="width:510px;"></el-input>
                                            </el-form-item>
                                            <el-form-item prop="caseState" label="用例状态:">
                                                <el-select v-model="BasicRomeData.caseState" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.caseStateOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item label="关联页面:">
                                               <el-cascader 
                                               style="width:825px"
                                               placeholder="如需要在选择元素中找到别的所属页面元素,可在此选择关联相对应页面"
                                               :options="BasicRomeData.associatedPage" :props="BasicRomeData.associatedProps" clearable></el-cascader>
                                            </el-form-item>
                                        </el-form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==1">
                        <div>
                            <el-table
                                ref="TestSetTableData"
                                id="TestSet" 
                                row-key="id"
                                :data="TestSetRomeData.tableData"
                                :row-class-name="tableRowClassName"
                                height="720px"
                                border>
                                <el-table-column
                                    label="序列"  
                                    type="index" 
                                    width="60" 
                                    align="center">
                                </el-table-column>
                                <el-table-column
                                    label="事件名称"
                                    align= "center"
                                    prop="eventName">
                                </el-table-column>
                                <el-table-column
                                    label="操作类型"
                                    align= "center"
                                    width="140" 
                                    prop="operationTypeTxt">
                                </el-table-column>
                                <el-table-column
                                    label="对比类型"
                                    align= "center"
                                    width="140" 
                                    prop="contrastTypeText">
                                </el-table-column>
                                <el-table-column
                                    label="输入/选择"
                                    show-overflow-tooltip
                                    align= "center"
                                    prop="inputText">
                                </el-table-column>
                                <el-table-column
                                    label="断言类型"
                                    align= "center"
                                    width="120"
                                    prop="assertType">
                                </el-table-column>
                                <el-table-column
                                    label="断言值类型"
                                    width="120"
                                    align= "center"
                                    prop="assertValueType">
                                </el-table-column>
                                <el-table-column
                                    label="断言值"
                                    width="200"
                                    align= "center"
                                    prop="assertValue">
                                </el-table-column>
                                <el-table-column 
                                    width="290" 
                                    align= "center">
                                    <template slot="header">
                                        <el-button-group>
                                            <el-button type="primary" @click="openCaseStepsDialog()">新增步骤</el-button>
                                            <el-button type="success" @click="handleAllDoe(1)">全启</el-button>
                                            <el-button type="warning" @click="handleAllDoe(0)">全禁</el-button>
                                        </el-button-group>
                                    </template>
                                    <template slot-scope="scope">
                                        <el-button-group>
                                            <el-button
                                                size="mini"
                                                @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                                            <el-button v-if="scope.row.doeValue==1" size="mini" type="info" @click="handleDoe(scope.$index, scope.row,0)">禁用</el-button>
                                            <el-button v-else size="mini" type="warning" @click="handleDoe(scope.$index, scope.row,1)">启用</el-button>
                                            <el-button
                                                size="mini"
                                                type="danger"
                                                @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                                        </el-button-group>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==2">
                      
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
            <dialog-case-steps
                @closeDialog="closeCaseStepsDialog" 
                :isVisible="dialog.caseSteps.dialogVisible" 
                :dialogPara="dialog.caseSteps.dialogPara">
            </dialog-case-steps>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import Sortable from 'sortablejs';
import {PrintConsole} from "../../../../../../js/Logger.js";

import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetPageEnvironmentNameItems} from "../../../../../../js/GetSelectTable.js";
import DialogCaseSteps from "./CaseSteps.vue";


export default {
    components: {
        DialogCaseSteps
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            StepsRomeData:{
                active:0,
                stepLength:4,//步长，整个窗口可以执行的步骤数
                processStatus:'process',
                disPlay_Save:false,
                disPlay_Next:true,
                disPlay_Previous:false,
            },
            BasicRomeData:{
                caseId:'',
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                environmentId:'',
                environmentNameOption:[],
                testType:'',
                testTypeOption:[
                    {'label':'单元测试','value':'UnitTest'},
                    {'label':'混合测试','value':'HybridTest'},
                ],
                labelId:'',
                labelNameOption:[
                    {'label':'普通用例','value':'CommonCase'},
                    {'label':'回归用例','value':'ReturnCase'},
                ],
                priorityId:'',//优先级
                priorityNameOption:[
                    {'label':'P0','value':'P0','details':'最高'},
                    {'label':'P1','value':'P1','details':'高'},
                    {'label':'P2','value':'P2','details':'中'},
                    {'label':'P3','value':'P3','details':'低'},
                ],
                caseState:'',
                caseStateOption:[
                    {'label':'研发中','value':'InDev'},
                    {'label':'已完成','value':'Completed'},
                    {'label':'弃用','value':'Discard'},
                ],
                caseName:'',
                associatedPage:[],
                associatedProps: { multiple: true },
                rules:{
                    pageId:[{ required: true, message: '请选择所属页面', trigger: 'change' }],
                    funId:[{ required: true, message: '请选择所属功能', trigger: 'change' }],
                    environmentId:[{ required: true, message: '请选择页面环境', trigger: 'change' }],
                    testType:[{ required: true, message: '请选择测试类型', trigger: 'change' }],
                    labelId:[{ required: true, message: '请选择用例标签', trigger: 'change' }],
                    priorityId:[{ required: true, message: '请选择优先级', trigger: 'change' }],
                    caseName:[
                        { required: true, message: '请输入用例名称', trigger: 'blur' },
                        { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' }
                    ],
                    caseState:[{ required: true, message: '请选择用例状态', trigger: 'change' }],
                },
            },
            TestSetRomeData:{
                tableData:[],
            },
          
            CharmRomeData:{
                title:'',
                tableData:[],
            },
            dialog:{
                caseSteps:{
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
                this.ClearTestSetRomeData();

                
                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew;

                if(newval.isAddNew==false){//进入编辑状态
                    this.BasicRomeData.caseId = newval.caseId;
      
                  
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
            }else if(newVal==2){
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
        'BasicRomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.BasicRomeData.funId='';
                self.BasicRomeData.funNameOption=[];
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
            if(self.StepsRomeData.active==0){//基本用例数据
                self.StepsRomeData.active++;
                // this.$refs['BasicRomeData'].validate((valid) => {
                //     if (valid) {//通过
                //         self.StepsRomeData.active++;
                //         self.$nextTick(function () {//当DOM加载完成后才会执行这个!
                //             self.rowDrop();
                //         })
                //     } 
                // });
            }else if(self.StepsRomeData.active==1){
                self.StepsRomeData.active++;
            }else if(self.StepsRomeData.active==2){
                self.StepsRomeData.active++;
            }
        },
        previous(){//上一步
            let self = this;
            self.StepsRomeData.processStatus='process';
            if(self.StepsRomeData.active==0){

            }else if(self.StepsRomeData.active==4){
                self.StepsRomeData.active--;
                self.StepsRomeData.active--;
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
            self.BasicRomeData.pageId='';
            self.BasicRomeData.funId='';
            self.BasicRomeData.environmentId='';
            self.BasicRomeData.testType='';
            self.BasicRomeData.labelId='';
            self.BasicRomeData.priorityId='';
            self.BasicRomeData.caseState='';
            self.BasicRomeData.caseName='';
            self.BasicRomeData.associatedPage=[];
        },
        GetPageNameOption(){
            GetPageNameItems(this.$cookies.get('proId')).then(d=>{
                this.BasicRomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            this.BasicRomeData.funNameOption = [];
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

        //测试集
        ClearTestSetRomeData(){
            let self = this;
            self.TestSetRomeData.tableData=[];
        },
        tableRowClassName({row, rowIndex}) {//禁用时 当前行显示为高亮
            if (row.state === false) {
                return 'warning-row';
            }
            return '';
        },
        closeCaseStepsDialog(){
            this.dialog.caseSteps.dialogVisible =false;
        },
        openCaseStepsDialog(){
            let self = this;
            self.dialog.caseSteps.dialogPara={
                dialogTitle:"新增步骤",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.caseSteps.dialogVisible=true;
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
