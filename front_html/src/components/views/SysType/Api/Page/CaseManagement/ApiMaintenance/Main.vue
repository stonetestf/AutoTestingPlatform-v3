<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <el-card class="MainCard">
                <template>
                    <el-form :inline="true" class="demo-form-inline" method="post">
                    <el-form-item label="所属页面:">
                        <el-select v-model="SelectRomeData.pageId" clearable placeholder="请选择" style="width:150px;" @click.native="GetPageNameOption()">
                            <el-option
                                v-for="item in SelectRomeData.pageNameOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="所属功能:">
                        <el-select v-model="SelectRomeData.funId" clearable placeholder="请选择" style="width:150px;" @click.native="GetFunNameOption()">
                            <el-option
                                v-for="item in SelectRomeData.funNameOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="接口名称:">
                        <el-input clearable v-model="SelectRomeData.apiName"></el-input>
                    </el-form-item>
                    <el-form-item label="接口地址:">
                        <el-input clearable v-model="SelectRomeData.requestUrl"></el-input>
                    </el-form-item>
                    <el-form-item label="接口状态:">
                        <el-select v-model="SelectRomeData.apiState" clearable placeholder="请选择" style="width:100px;">
                            <el-option
                                v-for="item in SelectRomeData.apiStateOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="关联对象:">
                        <el-select v-model="SelectRomeData.associations" clearable placeholder="请选择" style="width:100px;">
                            <el-option
                                v-for="item in SelectRomeData.associationsOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-button type="primary" @click="SelectData()" >查询</el-button>
                    <el-button type="info" @click="ClearSelectRomeData()">重置</el-button>
                    <!-- <div style="float:right"> -->
                        <!-- <el-button icon="el-icon-question" circle plain @click="helpMsg()"></el-button> -->
                    <!-- </div> -->
                </el-form>
                </template>
                <template>
                    <div style="margin-top:-15px;">
                    <el-table
                        v-loading="loading"
                        :data=tableData
                        height="630px"
                        border
                        ref="multipleTable"
                        @selection-change="handleSelectionChange"
                        @row-click="handleRowClick">
                        <el-table-column
                            type="selection"
                            align= "center"
                            width="50">
                        </el-table-column>
                        <!-- <el-table-column
                            label="ID"
                            align= "center"
                            width="80px"
                            prop="id">
                        </el-table-column> -->
                        <el-table-column
                            label="所属页面"
                            align= "center"
                            width="180px"
                            prop="pageName">
                        </el-table-column>
                        <el-table-column
                            label="所属功能"
                            align= "center"
                            width="180px"
                            prop="funName">
                        </el-table-column>
                        <el-table-column
                            label="接口名称"
                            width="300px"
                            align= "center"
                            prop="apiName">
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
                            show-overflow-tooltip
                            label="接口地址"
                            align= "center"
                            prop="requestUrl">
                        </el-table-column>
                        <el-table-column
                            label="接口状态"
                            width="100px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-tag type="info" v-if="scope.row.apiState=='InDev'" >研发中</el-tag>
                                <el-tag type="success" v-else-if="scope.row.apiState=='Completed'" >已完成</el-tag>
                                <el-tag type="danger" v-else>弃用</el-tag>
                            </template>
                        </el-table-column>   
                        <el-table-column
                            label="与我关联"
                            width="80px"
                            align= "center"
                            prop="associationMy">
                            <template slot-scope="scope">
                                <el-tag type="info" v-if="scope.row.associationMy">True</el-tag>
                            </template>
                        </el-table-column> 
                        <el-table-column
                            label="更新时间"
                            align= "center"
                            width="170px"
                            prop="updateTime">
                        </el-table-column>
                        <el-table-column
                            label="修改者"
                            align= "center"
                            width="100px"
                            prop="userName">
                        </el-table-column>
                        <el-table-column
                            align="center"
                            width="275px">
                        <template slot="header">
                            <el-button-group>  
                                <el-button type="primary" @click="OpenEditDialog()">新增</el-button>        
                                <el-dropdown @command="handleCommand">
                                    <el-button type="warning">
                                        更多菜单<i class="el-icon-arrow-down el-icon--right"></i>
                                    </el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item command="CopyApi">复制接口</el-dropdown-item>
                                        <el-dropdown-item command="SwaggerImport">Swagger导入</el-dropdown-item>
                                        <el-dropdown-item command="HistoryBack">历史恢复</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </el-button-group>
                        </template>
                        <template slot-scope="scope" style="width:100px">
                            <el-button-group>
                            <el-button
                                size="mini"
                                type="success"
                                @click="OpenRequestApiDialog(scope.$index, scope.row)">Request</el-button>
                            <el-button
                                type="warning"
                                size="mini"
                                @click="OpenWorkOrderDialog(scope.$index, scope.row)">工单</el-button>
                            <el-button
                                size="mini"
                                @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
                            <el-button
                                size="mini"
                                type="danger"
                                @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
                            </el-button-group>
                        </template>
                        </el-table-column>
                    </el-table>
                    </div>
                </template>
                <template>
                    <div style="margin-top:-10px">
                    <el-pagination background layout="total, sizes, prev, pager, next, jumper"
                        @size-change="pageSizeChange"
                        @current-change="handleCurrentChange"
                        :current-page="page.current" 
                        :total="page.total"
                        :page-sizes = [10,30,50,100]
                        style="margin: 20px auto auto auto;">
                    </el-pagination>
                    </div>
                </template>
            </el-card>
        </template>
        <template>
            <dialog-editor
                @closeDialog="closeEditDialog" 
                :isVisible="dialog.editor.dialogVisible" 
                :dialogPara="dialog.editor.dialogPara"
                @Succeed="SelectData">
            </dialog-editor>
        </template>
        <template>
            <dialog-request-api
                @closeDialog="closeRequestApiDialog" 
                :isVisible="dialog.requestApi.dialogVisible" 
                :dialogPara="dialog.requestApi.dialogPara"
                @Succeed="SelectData">
            </dialog-request-api>
        </template>
        <template>
            <dialog-work-order
                @closeDialog="closeWorkOrderDialog" 
                :isVisible="dialog.workOrder.dialogVisible" 
                :dialogPara="dialog.workOrder.dialogPara"
                @Succeed="SelectData">
            </dialog-work-order>
        </template>
        <template>
        <dialog-history-info
            @closeDialog="closeHistoryInfoDialog" 
            :isVisible="dialog.historyInfo.dialogVisible" 
            :dialogPara="dialog.historyInfo.dialogPara"
            @Succeed="SelectData">
        </dialog-history-info>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";
import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";
import DialogEditor from "./Editor.vue";
import DialogRequestApi from "./RequestApi.vue";
import DialogWorkOrder from "../../../../../WorkorderManagement/WorkorderMaintenance/Editor.vue";
import DialogHistoryInfo from "./HistoryInfo.vue";

export default {
    components: {
        DialogEditor,DialogRequestApi,DialogWorkOrder,DialogHistoryInfo
    },
    data() {
        return {
            loading:false,
            tableData: [],
            multipleSelection:[],
            SelectRomeData:{
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                apiName:'',
                requestUrl:'',
                apiState:'',
                apiStateOption:[
                    {'label':'研发中','value':'InDev'},
                    {'label':'已完成','value':'Completed'},
                    {'label':'弃用','value':'Discard'},
                ],
                associations:'',
                associationsOption:[
                    {'label':'我','value':'My'},
                    {'label':'全部','value':''},
                ],

            },
            RomeData:{
    
            },
            page: { 
                current: 1,// 默认显示第几页
                total: 0,// 总条数，根据接口获取数据长度(注意：这里不能为空)
                pageSize: 10, // 默认每页显示的条数（可修改）
            },
            dialog:{
                editor:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
                requestApi:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
                workOrder:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
                historyInfo:{
                dialogVisible:false,
                dialogPara:{
                    dialogTitle:"",//初始化标题
                    isAddNew:true,//初始化是否新增\修改
                },
                }
            },
           
        };
    },
    watch:{//当我们输入值后，wacth监听每次修改变化的新值，然后计算输出值
        'SelectRomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.SelectRomeData.funId='';
                self.SelectRomeData.funNameOption=[];
            }
        },
    },
    mounted(){
        this.SelectData();
    },
    methods: {
        SelectData(){
            let self = this;
            self.tableData= [];
            self.loading=true;
            self.$axios.get('/api/ApiIntMaintenance/SelectData',{
                params:{
                    "proId":self.$cookies.get('proId'),
                    "pageId":self.SelectRomeData.pageId,
                    "funId":self.SelectRomeData.funId,
                    "apiName":self.SelectRomeData.apiName,
                    "requestUrl":self.SelectRomeData.requestUrl,
                    'apiState':self.SelectRomeData.apiState,
                    'associations':self.SelectRomeData.associations,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.pageId=d.pageId;
                        obj.pageName = d.pageName;
                        obj.funId = d.funId;
                        obj.funName=d.funName;
                        obj.apiName = d.apiName;
                        obj.requestType = d.requestType;
                        obj.requestUrl = d.requestUrl;
                        obj.apiState =d.apiState;
                        obj.associationMy=d.associationMy;
                        obj.updateTime = d.updateTime;
                        obj.userName = d.userName;
                        obj.createUserId = d.createUserId;        

                        self.tableData.push(obj);
                    });
                    if(self.tableData.length==0 && self.page.current != 1){
                        self.page.current = 1;
                        self.SelectData();
                    }
                    self.page.total = res.data.Total;
                    self.loading=false;
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                    self.loading=false;
                }
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
        },
        handleCommand(command){//更多菜单
            PrintConsole(command);
            if(command=='CopyApi'){
                this.CopyApi();
            }else if(command=='HistoryBack'){
                this.OpenHistoryInfoDialog();
            }
        },
        closeEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增接口",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },
        closeRequestApiDialog(){
            this.dialog.requestApi.dialogVisible =false;
        },
        OpenRequestApiDialog(index,row){
            let self = this;
            self.dialog.requestApi.dialogPara={
                dialogTitle:'选择运行',//初始化标题
                apiId:row.id,
                apiName:row.apiName,
            }
            self.dialog.requestApi.dialogVisible=true;
        },
        closeWorkOrderDialog(){
            this.dialog.workOrder.dialogVisible =false;
        },
        OpenWorkOrderDialog(index,row){
            let self = this;
            self.dialog.workOrder.dialogPara={
                dialogTitle:'新增工单',//初始化标题
                isAddNew:true,
                triggerPage:'ApiMaintenance',//触发页面
                workType:'Other',
                workState:0,
                pageId:row.pageId,
                funId:row.funId,
                workName:row.apiName,
                createUserId:row.createUserId
            }
            self.dialog.workOrder.dialogVisible=true;
        },
        closeHistoryInfoDialog(){
        this.dialog.historyInfo.dialogVisible =false;
        },
        OpenHistoryInfoDialog(){
            let self = this;
            if(self.multipleSelection.length>1){
                self.$message.warning('只可勾选1条数据或不勾选数据进行历史查看及恢复!');
            }else{
                self.dialog.historyInfo.dialogPara={
                    dialogTitle:"历史恢复",//初始化标题
                    apiId:self.multipleSelection[0],
                }
                self.dialog.historyInfo.dialogVisible=true;
            }
        },
        GetPageNameOption(){
            GetPageNameItems(this.$cookies.get('proId')).then(d=>{
                this.SelectRomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            if(this.SelectRomeData.pageId){
                GetFunNameItems(this.$cookies.get('proId'),this.SelectRomeData.pageId).then(d=>{
                    this.SelectRomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.pageId='';
            self.SelectRomeData.funId='';
            self.SelectRomeData.apiName='';
            self.SelectRomeData.requestUrl='';
            self.SelectRomeData.apiState='';
            self.SelectRomeData.associations='';
            self.SelectData();
        },
        pageSizeChange(pageSize) {
            let self = this;
            self.page.current = 1;
            self.page.pageSize = pageSize;
        },
        // 显示第几页
        handleCurrentChange(val) {
            let self = this;
            // 改变默认的页数
            self.page.current=val
            self.SelectData();
        },
        handleDelete(index,row){
            this.$confirm('请确定是否删除?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                    this.DeleteData(row.id);     
                }).catch(() => {       
            });
        },
        DeleteData(id){
            let self = this;
            self.$axios.post('/api/ApiIntMaintenance/DeleteData',Qs.stringify({
                'apiId':id,
            })).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('接口删除成功!');
                self.SelectData();
            }
            else{
                self.$message.error('接口删除失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑接口",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                apiId:row.id,
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleRowClick(row, column, event){//点击行选择勾选框
          this.$refs.multipleTable.toggleRowSelection(row);
        },
        handleSelectionChange(val){//勾选数据时触发
            // console.log(val)
            this.multipleSelection=[];
            val.forEach(d =>{
                this.multipleSelection.push(d.id);
            }); 
        },
        CopyApi(){
            let self = this;
            if(self.multipleSelection.length==0){
                self.$message.warning('请勾选1条数据进行复制操作!');
            }else{
                self.loading=true;
                self.$axios.get('/api/ApiIntMaintenance/CopyApi',{
                    params:{
                        'apiId':self.multipleSelection[0]
                    }
                }).then(res => {
                    if(res.data.statusCode==2000){
                        self.$message.success('接口复制成功!');
                        self.SelectData();
                        self.loading=false;
                    }else{
                        self.$message.error('获取数据失败:'+res.data.errorMsg);
                        self.loading=false;
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.loading=false;
                })
            }
        },
    }
};
</script>

<style>
body {
    margin: 0;
}
</style>
