<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <el-card class="MainCard">
                <template>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="项目名称:">
                            <el-input clearable v-model.trim="RomeData.proName"></el-input>
                        </el-form-item>
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </template>
                <template>
                    <div style="margin-top:-15px;">
                        <el-table
                            :data="RomeData.tableData"
                            height="596px"
                            border>
                            <!-- <el-table-column
                                label="ID"
                                align= "center"
                                width="80px"
                                prop="id">
                            </el-table-column> -->
                            <el-table-column
                                label="项目名称"
                                align= "center"
                                prop="proName">
                            </el-table-column>
                            <el-table-column
                                label="备注"
                                align= "center"
                                prop="remarks">
                            </el-table-column>
                            <el-table-column
                                label="关联用户"
                                align= "center"
                                prop="methodName">
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
                                width="200px"
                                prop="userName">
                            </el-table-column>
                            <el-table-column
                                align="center"
                                width="150px">
                                <template slot="header">
                                    <el-button type="primary" @click="OpenEditDialog()">新增</el-button>
                                </template>
                                <template slot-scope="scope" style="width:100px">
                                    <el-button
                                        size="mini"
                                        @click="handleEdit(scope.$index, scope.row)">进入
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
                @closeDialog="closeEditDialog" 
                :isVisible="dialog.editor.dialogVisible" 
                :dialogPara="dialog.editor.dialogPara"
                @Succeed="SelectData">
            </dialog-editor>
        </template>
    </div>
</template>

<script>
// import store from '../../../../store/index'
import DialogEditor from "./Editor.vue";

export default {
    components: {
        DialogEditor
    },
    data() {
        return {
            RomeData:{
                proName:'',
                tableData:[],
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
                }
            },
           

        };
    },
    mounted(){
    
    },
    methods: {
        ClearSelectRomeData(){
            let self = this;
            self.RomeData.proName='';

            self.SelectData();
        },
        SelectData(){

        },
        closeEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增项目",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
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
.MainCard{
    height:750px ;
}
</style>
