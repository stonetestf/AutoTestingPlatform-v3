<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <el-card class="MainCard">
                <div>
                    <el-form :inline="true"  method="post">
                        <el-row>
                            <el-col :span="20">
                                <el-form-item label="任务名称:">
                                    <el-input clearable v-model.trim="SelectRomeData.batchName"></el-input>
                                </el-form-item>
                                <el-form-item label="报告状态:">
                                    <el-select v-model="SelectRomeData.reportState" clearable placeholder="请选择" style="width:120px;">
                                        <el-option
                                            v-for="item in SelectRomeData.reportStateOption"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-button type="primary" @click="SelectData()">查询</el-button>
                                <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                            </el-col>
                            <el-col :span="4">
                                <el-tag style="float:right">钩子接口地址:{{SelectRomeData.hookUrl}}/api/ApiBatchTask/RunHookTask?hookId=***&version=自定义</el-tag>
                            </el-col>
                        </el-row>
                    </el-form>
                </div>
                <div>
                    <div style="margin-top:-15px;">
                        <el-table
                            v-loading="loading"
                            :data="RomeData.tableData"
                            height="653px"
                            border
                            ref="multipleTable"
                            @selection-change="handleSelectionChange"
                            @row-click="handleRowClick">
                            <el-table-column
                                type="selection"
                                align= "center"
                                width="50">
                            </el-table-column>
                            <el-table-column
                                label="ID"
                                align= "center"
                                width="80px"
                                prop="id">
                            </el-table-column>
                            <el-table-column
                                label="任务名称"
                                width="300px"
                                align= "center"
                                prop="batchName">
                            </el-table-column>
                            <el-table-column
                                show-overflow-tooltip
                                label="备注"
                                width="300px"
                                align= "center"
                                prop="remarks">
                            </el-table-column>    
                            <el-table-column
                                label="任务数量"
                                width="100px"
                                align= "center"
                                prop="taskTotal">
                            </el-table-column>  
                            <el-table-column
                                label="钩子状态"
                                width="100px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.hookState">开启</el-tag>
                                    <el-tag type="danger" v-else>关闭</el-tag>
                                </template>
                            </el-table-column>      
                            <el-table-column
                                label="最后报告时间"
                                width="160px"
                                align= "center">
                                <template slot-scope="scope">
                                    <span type="success" v-if="scope.row.lastReportTime" >{{scope.row.lastReportTime}} ms</span>
                                    <el-tag v-else>无最新数据</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="最后报告状态"
                                width="110px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.lastReportStatus=='Pass'" >Pass</el-tag>
                                    <el-tag type="warning" v-else-if="scope.row.lastReportStatus=='Fail'">Fail</el-tag>
                                    <el-tag type="danger" v-else-if="scope.row.lastReportStatus=='Error'">Error</el-tag>
                                    <el-tag v-else>无最新数据</el-tag>
                                </template>
                            </el-table-column> 
                            <el-table-column
                                label="通过率"
                                width="80px"
                                align= "center"
                                prop="passRate">
                            </el-table-column> 
                            <el-table-column
                                label="更新时间"
                                align= "center"
                                width="200px"
                                prop="updateTime">
                            </el-table-column>   
                            <el-table-column
                                show-overflow-tooltip
                                label="修改者"
                                align= "center"
                                width="150px"
                                prop="userName">
                            </el-table-column>
                            <el-table-column
                                show-overflow-tooltip
                                label="创建者"
                                align= "center"
                                width="150px"
                                prop="createUserName">
                            </el-table-column>   
                            <el-table-column
                                fixed="right"
                                align="center"
                                width="250px">
                            <template slot="header">
                                <el-button-group>
                                    <el-button type="primary" @click="OpenEditDialog()">新增</el-button>
                                    <el-dropdown @command="handleCommand">
                                        <el-button type="warning">
                                            更多菜单<i class="el-icon-arrow-down el-icon--right"></i>
                                        </el-button>
                                        <el-dropdown-menu slot="dropdown">
                                            <el-dropdown-item command="ExecutiveLogging">执行记录(未开发)</el-dropdown-item>
                                            <el-dropdown-item command="CopyTask">复制批量任务(未开发)</el-dropdown-item>
                                            <el-dropdown-item command="TaskRestore">恢复批量任务(未开发)</el-dropdown-item>
                                        </el-dropdown-menu>
                                    </el-dropdown>
                                </el-button-group>
                            </template>
                            <template slot-scope="scope" style="width:100px">
                                <el-button-group>
                                    <el-button
                                        :loading="buttonLoading"
                                        size="mini"
                                        type="success"
                                        @click="RunBatch(scope.$index, scope.row)">RunBatch
                                    </el-button>
                                    <el-button
                                        size="mini"
                                        @click="handleEdit(scope.$index, scope.row)">Edit
                                    </el-button>
                                    <el-button
                                        size="mini"
                                        type="danger"
                                        @click="handleDelete(scope.$index, scope.row)">Delete
                                    </el-button>
                                </el-button-group>
                            </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
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
            </el-card>
        </template>
        <template>
            <dialog-editor
                @closeDialog="CloseEditDialog" 
                :isVisible="dialog.editor.dialogVisible" 
                :dialogPara="dialog.editor.dialogPara"
                @Succeed="SelectData">
            </dialog-editor>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import store from '../../../../../../../store/index';
import {PrintConsole} from "../../../../../../js/Logger.js";

import DialogEditor from "./Editor.vue";

export default {
    components: {
        DialogEditor
    },
    data() {
        return {
            loading:false,
            buttonLoading:false,
            multipleSelection:[],
            SelectRomeData:{
                batchName:'',
                reportState:'',
                reportStateOption:[
                    {'label':'Pass','value':'Pass'},
                    {'label':'Fail','value':'Fail'},
                    {'label':'Error','value':'Error'},
                ],
                hookUrl:store.state.BackService
            },
            RomeData:{
                tableData: [],
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
            },
          
        };
    },
    watch:{//当我们输入值后，wacth监听每次修改变化的新值，然后计算输出值
     
    },
    mounted(){
        this.SelectData();
    },
    methods: {
        SelectData(){//刷新列表数据
            let self = this;
            self.loading=true;
            self.RomeData.tableData= [];
            self.$axios.get('/api/ApiBatchTask/SelectData',{
                params:{
                    'proId':self.$cookies.get('proId'),
                    'batchName':self.SelectRomeData.batchName,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.batchName=d.batchName;
                        obj.remarks = d.remarks;
                        obj.taskTotal = d.taskTotal;
                        obj.hookState = d.hookState;
                        obj.lastReportTime = d.lastReportTime;
                        obj.lastReportStatus = d.lastReportStatus;
                        obj.passRate=d.passRate+'%';
                        obj.updateTime = d.updateTime;
                        obj.userName = d.userName;
                        obj.createUserName = d.createUserName;

                        self.RomeData.tableData.push(obj);
                    });
                    if(self.RomeData.tableData.length==0 && self.page.current != 1){
                        self.page.current = 1;
                        self.SelectData();
                    }
                    self.page.total = res.data.Total;
                    self.loading=false;
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                    self.loading=false;
                }
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
        },
        handleCommand(command){
            PrintConsole(command);
           
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.batchName='';
            self.SelectRomeData.reportState='';
            self.SelectData();
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
        CloseEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增批量任务",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑批量任务",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                batchId:row.id,
            }
            self.dialog.editor.dialogVisible=true;
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
            self.$axios.post('/api/ApiBatchTask/DeleteData',Qs.stringify({
                'batchId':id,
            })).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('删除定批量任务成功!');
                self.SelectData();
            }
            else{
                self.$message.error('删除批量任务失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
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
            self.page.current=val;
            self.SelectData();
        },
        RunBatch(index,row){
            let self = this;
            self.buttonLoading=true;
            self.$axios.post('/api/ApiBatchTask/ExecuteBatchTask',Qs.stringify({
                'batchId':row.id,
            })).then(res => {
            if(res.data.statusCode ==2001){
                self.$message.success('批量任务已启动,任务ID:'+res.data.celeryTaskId+',请稍后在测试报告页面查看结果!');
                self.buttonLoading=false;
            }
            else{
                self.$message.error('批量任务启动失败:'+ res.data.errorMsg);
                self.buttonLoading=false;
            }
            }).catch(function (error) {
                console.log(error);
                self.buttonLoading=false;
            })
        },
    }
};
</script>

<style>
.MainCard{
    height: 770px;
}
</style>
