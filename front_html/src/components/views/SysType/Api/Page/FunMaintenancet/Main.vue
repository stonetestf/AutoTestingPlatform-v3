<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <el-card class="MainCard">
                <template>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="所属项目:">
                            <el-select v-model="SelectRomeData.proId" clearable placeholder="请选择" style="width:200px;" @click.native="GetProNameOption()">
                                <el-option
                                    v-for="item in SelectRomeData.proNameOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="所属模块:">
                            <el-select v-model="SelectRomeData.moduleId" clearable placeholder="请选择" style="width:200px;" @click.native="GetModuleNameOption()">
                                <el-option
                                    v-for="item in SelectRomeData.moduleNameOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="页面名称:">
                            <el-input clearable v-model.trim="SelectRomeData.pageName"></el-input>
                        </el-form-item>
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </template>
                <template>
                    <div style="margin-top:-15px;">
                        <el-table
                            :data="tableData"
                            height="596px"
                            border>
                            <el-table-column
                                label="ID"
                                align= "center"
                                width="100px"
                                prop="id">
                            </el-table-column>
                            <el-table-column
                                label="页面名称"
                                align= "center"
                                prop="pageName">
                            </el-table-column>
                            <el-table-column
                                label="所属项目"
                                align= "center"
                                prop="proName">
                            </el-table-column>
                            <el-table-column
                                label="所属模块"
                                align= "center"
                                prop="moduleName">
                            </el-table-column>
                            <el-table-column
                                label="接口数量"
                                width="100px"
                                align= "center"
                                prop="intNum">
                            </el-table-column>
                            <el-table-column
                                label="备注"
                                align= "center"
                                prop="remarks">
                            </el-table-column>         
                            <el-table-column
                                label="更新时间"
                                align= "center"
                                width="200px"
                                prop="updateTime">
                            </el-table-column>   
                            <el-table-column
                                label="修改者"
                                align= "center"
                                width="150px"
                                prop="userName">
                            </el-table-column>   
                            <el-table-column
                                align="center"
                                width="200px">
                            <template slot="header">
                                <el-button type="primary" @click="OpenEditDialog_Edit()">新增</el-button>
                            </template>
                            <template slot-scope="scope" style="width:100px">
                                <el-button
                                    size="mini"
                                    @click="handleEdit(scope.$index, scope.row)">Edit
                                </el-button>
                                <el-button
                                    size="mini"
                                    type="danger"
                                    @click="handleDelete(scope.$index, scope.row)">Delete
                                </el-button>
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
                @closeDialog="closeDialog_Edit" 
                :isVisible="dialogVisible_editor" 
                :dialogPara="dialogPara_editor"
                @Succeed="SelectData">
            </dialog-editor>
        </template>
    </div>
</template>

<script>
// import store from '../../../../store/index'
import DialogEditor from "./Editor.vue";
// import {GetProNameItems} from "../../../js/intGetCommonTable.js";
// import {GetModuleNameItems} from "../../../js/intGetCommonTable.js";

export default {
    components: {
        DialogEditor,
    },
    data() {
        return {
            tableData: [],
            SelectRomeData:{
                proId:'',
                proNameOption:[],
                moduleId:'',
                moduleNameOption:[],
                pageName:'',
            },
            RomeData:{
    
            },
            page: { 
                current: 1,// 默认显示第几页
                total: 0,// 总条数，根据接口获取数据长度(注意：这里不能为空)
                pageSize: 10, // 默认每页显示的条数（可修改）
            },
            dialogVisible_editor:false,
            dialogPara_editor:{
                dialogTitle:"",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            },
        };
    },
    watch:{//当我们输入值后，wacth监听每次修改变化的新值，然后计算输出值
        'SelectRomeData.proId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            console.log('newVal:'+newVal)
            let self = this;
            if(newVal!=oldVal){
                self.SelectRomeData.moduleId='';
                self.SelectRomeData.moduleNameOption=[];
            }
        },
    },
    mounted(){
        this.SelectData();
    },
    methods: {
        SelectData(){//刷新列表数据
            let self = this;
            self.tableData= [];
            self.$axios.get('/api/Int_PageMaintenance/SelectData',{
                params:{
                    'proId':self.SelectRomeData.proId,
                    'moduleId':self.SelectRomeData.moduleId,
                    'pageName':self.SelectRomeData.pageName,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.pageName = d.pageName;
                        obj.proId = d.proId;
                        obj.proName = d.proName;
                        obj.moduleId = d.moduleId;
                        obj.moduleName = d.moduleName;
                        obj.intNum = d.intNum;
                        obj.remarks = d.remarks;
                        obj.updateTime = d.updateTime;
                        obj.userName = d.userName;

                        self.tableData.push(obj);
                    });
                    if(self.tableData.length==0 && self.page.current != 1){
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
        GetProNameOption(){
            GetProNameItems().then(d=>{
                this.SelectRomeData.proNameOption = d;
            });
        },
        GetModuleNameOption(){
            let self = this;
            if(self.SelectRomeData.proId){
                GetModuleNameItems(self.SelectRomeData.proId).then(d=>{
                    this.SelectRomeData.moduleNameOption = d;
                });
            }else{
                self.$message.warning('请先选择所属项目');
            }
        },
        closeDialog_Edit(){
            this.dialogVisible_editor =false;
        },
        OpenEditDialog_Edit(){
            let self = this;
            self.dialogPara_editor={
                dialogTitle:"新增页面",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialogVisible_editor=true;
        },
        handleEdit(index,row){
            let self = this;
            self.dialogPara_editor={
                dialogTitle:"编辑页面",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                pageId:row.id,
                proId:row.proId,
                moduleId:row.moduleId,
                pageName:row.pageName,
                remarks:row.remarks,
            }
            self.dialogVisible_editor=true;
        },
        handleDelete(index,row){
            this.$confirm('请确定是否删除?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                   this.DataDelete(row.id);     
                }).catch(() => {       
            });
        },
        DataDelete(id){
            let self = this;
            console.log(id)
            self.$axios.post('/api/Int_PageMaintenance/DataDelete',{
                'userId':store.state.userId,
                "data":{
                    'pageId':id,
                    }
            }).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('页面删除成功!');
                self.SelectData();
            }
            else{
                self.$message.error('页面删除失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.proId='';
            self.SelectRomeData.moduleId='';
            self.SelectRomeData.pageName='';
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
        },
    }
};
</script>

<style>

</style>
