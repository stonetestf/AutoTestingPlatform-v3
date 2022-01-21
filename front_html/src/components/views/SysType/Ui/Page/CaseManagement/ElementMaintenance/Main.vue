<template>
    <div>
        <template>
            <el-card class="MainCard">
                <div>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="所属页面:">
                            <el-select v-model="SelectRomeData.pageId" clearable placeholder="请选择" style="width:200px;" @click.native="GetModuleNameOption()">
                                <el-option
                                    v-for="item in SelectRomeData.pageNameOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="所属功能:">
                            <el-select v-model="SelectRomeData.funId" clearable placeholder="请选择" style="width:200px;" @click.native="GetPageNameOption()">
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
                        v-loading="loading"
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
                                            type="index"
                                            label="Index"
                                            align= "center"
                                            width="80">
                                        </el-table-column>
                                        <el-table-column
                                            label="状态"
                                            align= "center"
                                            width="100">
                                            <template slot-scope="scope">
                                                <el-tag type="success" v-if="scope.row.state">启用</el-tag>
                                                <el-tag type="danger" v-else>禁用</el-tag>
                                            </template>
                                        </el-table-column>
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
                            width="300px"
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
                            width="160px"
                            prop="elementType">
                        </el-table-column>
                        <el-table-column
                            label="定位数量"
                            align= "center"
                            width="100px"
                            prop="locationTotal">
                        </el-table-column>
                        <el-table-column
                            label="元素状态"
                            align= "center"
                            width="100px">
                            <template slot-scope="scope">
                                <el-tag type="success" v-if="scope.row.elementState">启用</el-tag>
                                <el-tag type="info" v-else>禁用</el-tag>
                            </template>
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
                            fixed="right"
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
                            <el-button-group>
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
import Qs from 'qs';
import {PrintConsole} from '../../../../../../js/Logger';
import DialogEditor from "./Editor.vue";

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
                elementName:'',
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
            let self = this;
            self.loading=true;
            self.tableData= [];
            self.$axios.get('/api/UiElementMaintenance/SelectData',{
                params:{
                    'proId':self.$cookies.get('proId'),
                    'pageId':self.SelectRomeData.pageId,
                    'funId':self.SelectRomeData.funId,
                    'elementName':self.SelectRomeData.elementName,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.elementName=d.elementName;
                        obj.pageName = d.pageName;
                        obj.funName = d.funName;
                        obj.elementType = d.elementType;
                        obj.locationTotal = d.locationTotal;
                        obj.elementState=d.elementState;
                        obj.updateTime = d.updateTime;
                        obj.userName = d.userName;
                        obj.createUserName = d.createUserName;
                        obj.tableItem=d.tableItem;

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
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
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
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑元素",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                elementId:row.id,
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
            self.$axios.post('/api/UiElementMaintenance/DeleteData',Qs.stringify({
                'elementId':id,
            })).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('删除元素成功!');
                self.SelectData();
            }
            else{
                self.$message.error('删除元素失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
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
