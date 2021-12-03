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
                        <el-input clearable v-model="SelectRomeData.apiUrl"></el-input>
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
                        height="600px"
                        border>
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
                            prop="moduleName">
                        </el-table-column>
                        <el-table-column
                            label="所属功能"
                            align= "center"
                            width="180px"
                            prop="pageName">
                        </el-table-column>
                        <el-table-column
                            label="接口名称"
                            width="300px"
                            align= "center"
                            prop="intName">
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
                                <el-tag type="info" v-if="scope.row.intState=='0'" >研发中</el-tag>
                                <el-tag type="success" v-else-if="scope.row.intState=='1'" >已完成</el-tag>
                                <el-tag type="danger" v-else>弃用</el-tag>
                            </template>
                        </el-table-column>   
                        <el-table-column
                            label="关联对象"
                            width="80px"
                            align= "center"
                            prop="intName">
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
                            width="230px">
                        <template slot="header">
                            <el-button-group>  
                                <el-button type="primary" @click="OpenEditDialog()">新增</el-button>        
                                <el-dropdown @command="handleCommand">
                                    <el-button type="warning">
                                        更多菜单<i class="el-icon-arrow-down el-icon--right"></i>
                                    </el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item command="CopyInt">复制接口</el-dropdown-item>
                                        <el-dropdown-item command="SwaggerImport">Swagger导入</el-dropdown-item>
                                        <el-dropdown-item command="CopyInt">历史恢复</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </el-button-group>
                        </template>
                        <template slot-scope="scope" style="width:100px">
                        <el-button
                            size="mini"
                            type="success"
                            @click="RequestIns(scope.$index, scope.row)">Run</el-button>
                        <el-button
                            size="mini"
                            @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
                        <el-button
                            size="mini"
                            type="danger"
                            @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
                        </template>
                        </el-table-column>
                    </el-table>
                    </div>
                </template>
                <template>
                    <el-pagination background layout="total, sizes, prev, pager, next, jumper"
                        @size-change="pageSizeChange"
                        @current-change="handleCurrentChange"
                        :current-page="page.current" 
                        :total="page.total"
                        :page-sizes = [10,30,50,100]
                        style="margin: 20px auto auto auto;">
                    </el-pagination>
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
    </div>
</template>

<script>
import {PrintConsole} from "../../../../../../js/Logger.js";
import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";
// import store from '../../../../store/index'
import DialogEditor from "./Editor.vue";
// import DialogRequestInt from "./RequestInt.vue";


export default {
    components: {
        DialogEditor
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
                apiUrl:'',
                apiState:'',
                apiStateOption:[
                    {'label':'研发中','value':'InDev'},
                    {'label':'已完成','value':'Completed'},
                    {'label':'弃用','value':'Discard'},
                ],
                associations:'',
                associationsOption:[
                    {'label':'我','value':'My'},
                    {'label':'全部','value':'All'},
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
        // this.SelectData();
    },
    methods: {
        SelectData(){
            let self = this;
            // self.tableData= [];
            // self.loading=true;
            // self.$axios.get('/api/Int_InsManagement/SelectData',{
            //     params:{
            //         "proId":self.SelectRomeData.proId,
            //         "moduleId":self.SelectRomeData.moduleId,
            //         "pageId":self.SelectRomeData.pageId,
            //         "insName":self.SelectRomeData.insName,
            //         "requestUrl":self.SelectRomeData.requestUrl,
            //         'intState':self.SelectRomeData.intState,
            //         'current':self.page.current,
            //         'pageSize':self.page.pageSize
            //     }
            // }).then(res => {
            //     if(res.data.statusCode==2000){
            //         res.data.TableData.forEach(d => {
            //             let obj = {};
            //             obj.id =d.id;
            //             obj.proId = d.proId;
            //             obj.moduleId=d.moduleId;
            //             obj.pageId = d.pageId;
            //             obj.proName = d.proName;
            //             obj.moduleName = d.moduleName;
            //             obj.pageName =d.pageName;
            //             obj.intName = d.intName;
            //             obj.requestUrl=d.requestUrl;
            //             obj.requestType = d.requestType;
            //             obj.intState = d.intState;
            //             obj.updateTime = d.updateTime;
            //             obj.userName = d.userName;

            //             self.tableData.push(obj);
            //         });
            //         if(self.tableData.length==0 && self.page.current != 1){
            //             self.page.current = 1;
            //             self.SelectData();
            //         }
            //         self.page.total = res.data.Total;
            //         self.loading=false;
            //     }else{
            //         self.$message.error('获取数据失败:'+res.data.errorMsg);
            //         self.loading=false;
            //     }
            // }).catch(function (error) {
            //     console.log(error);
            //     self.loading=false;
            // })
        },
        handleCommand(command){//更多菜单
            PrintConsole(command);
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
            self.SelectRomeData.apiUrl='';
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
    }
};
</script>

<style>
body {
    margin: 0;
}
</style>
