<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <el-card style="height: 760px;">
                <div style="margin-top:-10px">
                    <el-form :inline="true"  method="post">
                        <el-form-item label="任务名称:">
                            <el-input clearable v-model.trim="SelectRomeData.taskName"></el-input>
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
                    </el-form>
                </div>
                <div>
                    <div style="margin-top:-15px;">
                        <el-table
                            :data="RomeData.tableData"
                            height="653px"
                            border>
                            <!-- <el-table-column
                                type="selection"
                                align= "center"
                                width="50">
                            </el-table-column> -->
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
                                prop="taskName">
                            </el-table-column>
                            <el-table-column
                                label="定时配置"
                                width="200px"
                                align= "center"
                                prop="timingConfig">
                            </el-table-column>
                            <el-table-column
                                label="任务数量"
                                width="100px"
                                align= "center"
                                prop="taskSetTotal">
                            </el-table-column>
                            <el-table-column
                                show-overflow-tooltip
                                label="备注"
                                width="300px"
                                align= "center"
                                prop="remarks">
                            </el-table-column>      
                            <el-table-column
                                label="任务状态"
                                width="100px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.taskStatus" >启用</el-tag>
                                    <el-tag type="info" v-else>禁用</el-tag>
                                </template>
                            </el-table-column>          
                            <el-table-column
                                label="最后报告时间"
                                width="160px"
                                align= "center"
                                prop="lastReportTime">
                            </el-table-column>
                            <el-table-column
                                label="最后报告状态"
                                width="110px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.lastReportStatus=='Pass'" >Pass</el-tag>
                                    <el-tag type="warning" v-else-if="scope.row.lastReportStatus=='Fail'">Fail</el-tag>
                                    <el-tag type="danger" v-else-if="scope.row.lastReportStatus=='Error'">Error</el-tag>
                                    <el-tag v-else>未运行</el-tag>
                                </template>
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
                                width="230px">
                            <template slot="header">
                                <el-button-group>
                                    <el-button type="primary" @click="OpenEditDialog()">新增</el-button>
                                    <el-dropdown @command="handleCommand">
                                        <el-button type="warning">
                                            更多菜单<i class="el-icon-arrow-down el-icon--right"></i>
                                        </el-button>
                                        <el-dropdown-menu slot="dropdown">
                                            <el-dropdown-item command="CopyCase">复制任务</el-dropdown-item>
                                            <el-dropdown-item command="CaseRestore">恢复任务</el-dropdown-item>
                                        </el-dropdown-menu>
                                    </el-dropdown>
                                </el-button-group>
                            </template>
                            <template slot-scope="scope" style="width:100px">
                                <el-button-group>
                                    <el-button
                                        size="mini"
                                        type="success"
                                        @click="OpenRunTypeDialog(scope.$index, scope.row)">RunTask
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
import Qs from 'qs'
import {PrintConsole} from "../../../../../../js/Logger.js";

import DialogEditor from "./Editor.vue";

export default {
    components: {
        DialogEditor
    },
    data() {
        return {
            SelectRomeData:{
                taskName:'',
                reportState:'',
                reportStateOption:[
                    {'label':'Pass','value':'Pass'},
                    {'label':'Fail','value':'Fail'},
                    {'label':'Error','value':'Error'},
                ],
            },
            RomeData:{
                tableData: [
                    // {'id':'1','taskName':'测试任务','timingConfig':'* * * * *','taskTotal':8,'remarks':'这是备注啊','taskStatus':true,'lastReportTime':'2021-22-22 12:22:21',
                    // 'lastReportStatus':'Pass','updateTime':'2021-22-22 12:22:21','userName':'liepnglo(古雨辰)','createUserName':'lipenglo'},
                    // {'id':'2','taskName':'测试任务','timingConfig':'* * * * *','taskTotal':8,'remarks':'这是备注啊','taskStatus':false,'lastReportTime':'2021-22-22 12:22:21',
                    // 'lastReportStatus':'Fail','updateTime':'2021-22-22 12:22:21','userName':'liepnglo(古雨辰)','createUserName':'lipenglo'},
                ],
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
            self.RomeData.tableData= [];
            self.$axios.get('/api/ApiTimingTask/SelectData',{
                params:{
                    'proId':self.$cookies.get('proId'),
                    'taskName':self.SelectRomeData.taskName,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.taskName=d.taskName;
                        obj.timingConfig=d.timingConfig;
                        obj.taskSetTotal=d.taskSetTotal;
                        obj.remarks = d.remarks;
                        obj.taskStatus = d.taskStatus;
                        obj.lastReportTime = d.lastReportTime;
                        obj.lastReportStatus = d.lastReportStatus;
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
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                }
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
            })
        },
        CloseEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增任务",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑定时任务",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                taskId:row.id,
            }
            self.dialog.editor.dialogVisible=true;
        },
        // handleRowClick(row, column, event){//点击行选择勾选框
        // this.$refs.multipleTable.toggleRowSelection(row);
        // },
        // handleSelectionChange(val){//勾选数据时触发
        //     // console.log(val)
        //     this.multipleSelection=[];
        //     val.forEach(d =>{
        //         this.multipleSelection.push(d.id);
        //     }); 
        // },
        // handleDelete(index,row){
        //     this.$confirm('请确定是否删除?', '提示', {
        //         confirmButtonText: '确定',
        //         cancelButtonText: '取消',
        //         type: 'warning'
        //         }).then(() => {
        //            this.DeleteData(row.id);     
        //         }).catch(() => {       
        //     });
        // },
        // DeleteData(id){
        //     let self = this;
        //     self.$axios.post('/api/FunManagement/DeleteData',Qs.stringify({
        //         'funId':id,
        //     })).then(res => {
        //     if(res.data.statusCode ==2003){
        //         self.$message.success('删除功能成功!');
        //         self.SelectData();
        //     }
        //     else{
        //         self.$message.error('删除功能失败:'+ res.data.errorMsg);
        //     }
        //     }).catch(function (error) {
        //         console.log(error);
        //     })
        // },
        handleCommand(command){
            PrintConsole(command);
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.taskName='';
            self.SelectRomeData.reportState='';
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
            self.page.current=val;
            self.SelectData();
        },
    }
};
</script>

<style>
</style>
