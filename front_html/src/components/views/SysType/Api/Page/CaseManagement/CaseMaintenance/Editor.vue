<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="1500px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :close-on-press-escape="false"
            :before-close="dialogClose">
                <el-steps :active="StepsRomeData.active" simple :process-status="StepsRomeData.processStatus" finish-status="success">
                    <el-step title="维护基本信息"></el-step>
                    <el-step title="编写测试集"></el-step>
                    <el-step title="效验用例参数"></el-step>
                </el-steps>
                <el-card style="height:755px"
                    v-loading="loading"
                    element-loading-text="拼命加载中"
                    element-loading-spinner="el-icon-loading">
                    <template v-if="StepsRomeData.active==0">
                        <div class="table">
                           <div class="father" style="width: 100%; height: 600px;">
                                <div class="son" style="width: 950px; height: 150px;">
                                    <el-card style="width:1000px" shadow="never">
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
                                        </el-form>
                                    </el-card>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==1">
                        <div style="width:1411px;margin-left:30px">
                            <el-table
                                id="TestSet" 
                                row-key="id"
                                :data="TestSetRomeData.tableData"
                                height="710px"
                                border>
                                <el-table-column
                                    label="顺序"
                                    align= "center"
                                    type="index"
                                    width="80">
                                </el-table-column>
                                <el-table-column
                                    label="接口名称"
                                    align= "center"
                                    width="500px"
                                    prop="apiName">
                                </el-table-column>
                                <el-table-column
                                    label="测试名称"
                                    align= "center"
                                    width="300px">
                                    <template slot-scope="scope">
                                        <el-input v-model="scope.row.testName" maxlength="15" clearable show-word-limit placeholder="例:异常的登录"></el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    label="是否同步"
                                    align= "center"
                                    width="90px">
                                    <template slot-scope="scope">
                                    <el-switch v-model="scope.row.is_synchronous" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                        <el-tooltip placement="right">
                                            <div slot="content">此为单向同步,开启后只会同步:URL,请求的入参,不会同步参数值!<br/>开启时:在接口维护中修改此接口入参时,此接口在被用例运行时会以接口维护中的 <b>入参</b> 为准!<br/>关闭时:双向参数信息为独立!</div>
                                            <i class='el-icon-info'></i>
                                        </el-tooltip>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    label="接口状态"
                                    width="100px"
                                    align= "center">
                                    <template slot-scope="scope">
                                        <el-tag type="warning" v-if="scope.row.apiState=='InDev'" >研发中</el-tag>
                                        <el-tag type="success" v-else-if="scope.row.apiState=='Completed'" >已完成</el-tag>
                                        <el-tag type="info" v-else>弃用</el-tag>
                                    </template>
                                </el-table-column>   
                                <el-table-column
                                    label="设置参数"
                                    width="100px"
                                    align= "center">
                                    <template slot-scope="scope">
                                        <el-tag type="success" v-if="scope.row.paramsState" >已设置</el-tag>
                                        <el-tag type="warning" v-else>未设置</el-tag>
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
                                    width="150px">
                                    <template slot="header">
                                        <el-button type="primary" @click="OpenApiMainDialog()">新增</el-button>
                                    </template>
                                    <template slot-scope="scope" style="width:100px">
                                        <el-button
                                            type="success"
                                            size="mini"
                                            @click="OpenRequestParamsDialog(scope.$index, scope.row)">参数
                                        </el-button>
                                        <el-button
                                            size="mini"
                                            type="danger"
                                            @click="handleDelete(scope.$index, scope.row)">移除
                                        </el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </template>
                    <template v-else>
         
                    </template>
                </el-card>
                <el-button style="margin-top: 12px;" icon="el-icon-arrow-left" type="primary" v-if="StepsRomeData.disPlay_Previous" @click="previous">上一步</el-button>
                <el-button style="margin-top: 12px;" type="primary" v-if="StepsRomeData.disPlay_Next" @click="next">下一步<i class="el-icon-arrow-right el-icon--right"></i></el-button>
                <el-button style="margin-top: 12px;" type="success" v-if="StepsRomeData.disPlay_Save" @click="DataSave()">保存</el-button>
            </el-drawer>
        </template>
        <template>
            <dialog-api-main
                @closeDialog="closeApiMainDialog" 
                :isVisible="dialog.apiMain.dialogVisible" 
                :dialogPara="dialog.apiMain.dialogPara"
                @getData="AddToTestSetTable($event)">
            </dialog-api-main>
        </template>
        <template>
            <dialog-request-params
                @closeDialog="closeRequestParamsDialog" 
                :isVisible="dialog.requestParams.dialogVisible" 
                :dialogPara="dialog.requestParams.dialogPara"
                @getData="AddRequestParamsToTable($event)">
            </dialog-request-params>
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

import DialogApiMain from "./ApiMain.vue";
import DialogRequestParams from "./RequestParams.vue";


export default {
    components: {
        DialogApiMain,DialogRequestParams
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
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                labelId:'',
                labelNameOption:[
                    {'label':'普通用例','value':'CommonCase'},
                    {'label':'回归用例','value':'ReturnCase'},
                ],
                testType:'',
                testTypeOption:[
                    {'label':'单元测试','value':'UnitTest'},
                    {'label':'混合测试','value':'HybridTest'},
                ],
                caseState:'',
                caseStateOption:[
                    {'label':'研发中','value':'InDev'},
                    {'label':'已完成','value':'Completed'},
                    {'label':'弃用','value':'Discard'},
                ],
                environmentId:'',
                environmentNameOption:[],
                caseName:'',
                priorityId:'',//优先级
                priorityNameOption:[
                    {'label':'P0','value':'P0','details':'最高'},
                    {'label':'P1','value':'P1','details':'高'},
                    {'label':'P2','value':'P2','details':'中'},
                    {'label':'P3','value':'P3','details':'低'},
                ],
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
                tableData:[],//测试集数据
                newTableData:[]//重新组合测试集数据
            },
            dialog:{
                apiMain:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
                requestParams:{
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
                this.ClearTestSetRomeData();
                
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
                // this.$refs['BasicCase'].validate((valid) => {
                //     if (valid) {//通过
                //         self.StepsRomeData.active++;
                //         self.$nextTick(function () {//当DOM加载完成后才会执行这个!
                //             self.rowDrop();
                //         })
                //     } 
                // });
            }else if(self.StepsRomeData.active==1){
                if(self.TestSetRomeData.tableData.length<1){
                    self.$message.warning('当前至少新增1条接口数据!');
                }else{
                    if(self.TestSetRomeData.newTableData.length!=self.TestSetRomeData.tableData.length){
                        self.$message.warning('当前测试集中,有未编写的参数数据,请点击参数进行编写完成后在执行下一步操作!');
                    }else{
                        self.UpdateTestNameToTable();
                        PrintConsole('最终数据:',self.TestSetRomeData.newTableData);
                        self.StepsRomeData.active++;
                    }
                }
            }else{
                
                self.StepsRomeData.active++;
            }
        },
        previous(){//上一步
            let self = this;
            self.StepsRomeData.processStatus='process';
            self.StepsRomeData.active--;
            if(self.StepsRomeData.active==3){
                self.StepsRomeData.active--;
            }else if(self.StepsRomeData.active==1){
                // self.$nextTick(function () {//当DOM加载完成后才会执行这个!
                //     self.rowDrop();
                // })
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
            self.BasicRomeData.caseName='';
            self.BasicRomeData.caseState='';
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
                console.log('清除正则验证')
                this.$refs[formName].resetFields();
            }
        },

        //组合测试集
        ClearTestSetRomeData(){
            let self = this;
            self.TestSetRomeData.tableData=[];
            self.TestSetRomeData.newTableData=[];
            PrintConsole('ClearTestSetRomeData');
        },
        closeApiMainDialog(){
            this.dialog.apiMain.dialogVisible = false;
        },
        OpenApiMainDialog(){
            let self = this;
            self.dialog.apiMain.dialogPara={
                dialogTitle:"导入接口",//初始化标题
                pageId:self.BasicRomeData.pageId,
                funId:self.BasicRomeData.funId,
            }
            self.dialog.apiMain.dialogVisible=true;
        },
        AddToTestSetTable(data){
            let self = this;
            PrintConsole('回调数据:',data);
            //将重复的id给用 id-次数来处理
            let findCount = 0;
            data.forEach(item=>{
                let apiId = null;
                self.TestSetRomeData.tableData.forEach((d,i)=>{
                    if(d.id == item.id || d.id == item.id+'-'+findCount){
                        findCount++;
                    }
                });
                if(findCount!=0){
                    apiId=item.id+'-'+findCount;
                }else{
                    apiId=item.id;
                }
                let obj = {};
                obj.id=String(apiId);
                obj.state=true;
                obj.apiName=item.apiName;
                obj.apiState = item.apiState;
                obj.testName='';
                obj.is_synchronous=false;
                self.TestSetRomeData.tableData.push(obj);
            });
            self.rowDrop();
            PrintConsole('AddToTestSetTable:',self.TestSetRomeData.tableData);
        },
        handleDelete(index,row){//删除独条的步骤'
            let self = this;
            this.$confirm('请确定是否移除此条数据?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                    self.TestSetRomeData.tableData.splice(index,1);
                    self.TestSetRomeData.newTableData.forEach((d,i)=>{
                        if(d.apiId==row.id){
                            self.TestSetRomeData.newTableData.splice(i,1);
                        }
                    });
                    PrintConsole('最终数据:',self.TestSetRomeData.newTableData);
                }).catch(() => {       
            });
           
        },
        rowDrop() {//排序方法
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#TestSet > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.TestSetRomeData.tableData.splice(oldIndex, 1)[0];
                    self.TestSetRomeData.tableData.splice(newIndex, 0, currRow);
                    // console.log(self.RomeData.TableData);
                }
            });
        },
        AddRequestParamsToTable(data){//回调函数,把接口的请求数据返回到测试集页面的最终列表中
            PrintConsole('回调数据:',data);
            let self = this;
            let tempCaseTable = self.TestSetRomeData.newTableData.find(item=>
                item.apiId == data.apiId
            );
            //查询最终列表中有没有此数据,有就覆盖,没有就新增
            if(tempCaseTable){
                self.TestSetRomeData.newTableData.forEach((d,i)=>{
                    if(d.apiId==data.apiId){
                        self.TestSetRomeData.newTableData[i].requestType = data.requestType;
                        self.TestSetRomeData.newTableData[i].requestUrl = data.requestUrl;
                        
                        self.TestSetRomeData.newTableData[i].headers = data.headers;
                        self.TestSetRomeData.newTableData[i].params = data.params;

                        self.TestSetRomeData.newTableData[i].body.requestSaveType = data.body.requestSaveType;
                        self.TestSetRomeData.newTableData[i].body.formData = data.body.formData;
                        self.TestSetRomeData.newTableData[i].body.rawValue = data.body.rawValue;

                        self.TestSetRomeData.newTableData[i].extract = data.extract;
                        self.TestSetRomeData.newTableData[i].validate =data.validate;

                        self.TestSetRomeData.newTableData[i].preOperation =data.preOperation;
                        self.TestSetRomeData.newTableData[i].rearOperation =data.rearOperation;
                    }
                });
                PrintConsole('覆盖数据');
            }else{
                self.TestSetRomeData.newTableData.push(data);
                PrintConsole('新增数据');
            }
            PrintConsole('数据',self.TestSetRomeData.newTableData);
        },
        closeRequestParamsDialog(){
            this.dialog.requestParams.dialogVisible = false;
        },
        OpenRequestParamsDialog(index,row){
            let self = this;
            let dialogTitle = '';
            if(row.testName){
                dialogTitle = row.apiName+'('+row.testName+')';
            }else{
                dialogTitle = row.apiName;
            }
            
            self.dialog.requestParams.dialogPara={
                dialogTitle:dialogTitle,//初始化标题
                apiId:row.id,
                testName:row.testName,
                synchronous:row.is_synchronous,
                state:row.state,
                tableData:self.TestSetRomeData.newTableData,
            }
            self.dialog.requestParams.dialogVisible=true;
        },     
        UpdateTestNameToTable(){//更新测试名称和接口的状态到最终列表,在下一步的时候使用
            let self = this;
            self.TestSetRomeData.tableData.forEach(item=>{
                self.TestSetRomeData.newTableData.forEach((d,i)=>{
                    if(d.apiId == item.id){
                        self.TestSetRomeData.newTableData[i].synchronous = item.is_synchronous;
                        self.TestSetRomeData.newTableData[i].testName = item.testName;
                        self.TestSetRomeData.newTableData[i].state = item.state;
                    }
                });
               
            });
            PrintConsole('更新测试名称');
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
