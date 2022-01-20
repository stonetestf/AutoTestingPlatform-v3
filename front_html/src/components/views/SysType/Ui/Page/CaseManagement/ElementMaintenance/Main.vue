<template>
    <div>
        <template>
            <el-card class="MainCard">
                <div>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="所属页面:">
                            <el-select v-model="SelectRomeData.pageName" clearable placeholder="请选择" style="width:200px;" @click.native="GetModuleNameOption()">
                                <el-option
                                    v-for="item in SelectRomeData.pageNameOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="所属功能:">
                            <el-select v-model="SelectRomeData.funName" clearable placeholder="请选择" style="width:200px;" @click.native="GetPageNameOption()">
                                <el-option
                                    v-for="item in SelectRomeData.funNameOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="元素名称:">
                            <el-input clearable v-model.trim="SelectRomeData.elementName"></el-input>
                        </el-form-item>
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </div>
                <div style="margin-top:-15px;">
                    <el-table
                        :data="tableData"
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
                            label="详情" 
                            width="50px"
                            type="expand">
                            <template slot-scope="props">
                                <el-form label-position="left" >
                                    <el-table
                                        :data="props.row.tableItem"
                                        border>
                                        <el-table-column
                                            prop="targetingType"
                                            label="定位类型"
                                            align= "center"
                                            width="100">
                                        </el-table-column>
                                        <el-table-column
                                            prop="targetingPath"
                                            align= "center"
                                            label="定位地址">
                                        </el-table-column>
                                        <el-table-column
                                            prop="remarks"
                                            align= "center"
                                            label="备注信息">
                                        </el-table-column>
                                    </el-table>
                                </el-form>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="元素名称"
                            align= "center"
                            prop="elementName">
                        </el-table-column>
                        <el-table-column
                            label="所属页面"
                            width="200px"
                            align= "center"
                            prop="pageName">
                        </el-table-column>
                        <el-table-column
                            label="所属功能"
                            width="200px"
                            align= "center"
                            prop="funName">
                        </el-table-column>
                        <el-table-column
                            label="元素类型"
                            align= "center"
                            width="120px"
                            prop="elementType">
                        </el-table-column>
                        <el-table-column
                            label="定位数量"
                            align= "center"
                            width="100px"
                            prop="targetingTotal">
                        </el-table-column>
                        <el-table-column
                            label="更新时间"
                            width="160px"
                            align= "center"
                            prop="updateTime">
                        </el-table-column>
                        <el-table-column
                            label="修改者"
                            width="150px"
                            align= "center"
                            prop="userName">
                        </el-table-column>
                        <el-table-column
                            label="创建者"
                            align= "center"
                            width="150px"
                            prop="createUserName">
                        </el-table-column>
                        <el-table-column
                            align="center"
                            width="210px">
                        <template slot="header">
                            <el-button-group>
                                <el-button type="primary" @click="OpenEditDialog()">新增</el-button>
                                <el-dropdown @command="handleCommand">
                                    <el-button type="warning">
                                        更多菜单<i class="el-icon-arrow-down el-icon--right"></i>
                                    </el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item command="SwaggerImport">导入(Swagger)</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </el-button-group>
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
                @closeDialog="closeEditDialog" 
                :isVisible="dialog.editor.dialogVisible" 
                :dialogPara="dialog.editor.dialogPara"
                @Succeed="SelectData">
            </dialog-editor>
        </template>
    </div>
</template>

<script>
import { PrintConsole } from '../../../../../../js/Logger';
import DialogEditor from "./Editor.vue";

export default {
    components: {
       DialogEditor
    },
    data() {
        return {
            tableData: [],
            multipleSelection:[],
            SelectRomeData:{
                pageName:'',
                pageNameOption:[],
                funName:'',
                funNameOption:[],
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
        SelectData(){

        },
        //编辑、新增
        closeEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增元素",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleCommand(command){
            PrintConsole(command);

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
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.pageName='';
            self.SelectRomeData.funName='';
            self.SelectRomeData.elementName='';
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
.MainCard{
    height: 770px;
}
</style>
