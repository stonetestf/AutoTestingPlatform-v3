<template>
    <div ref="tab-main"  id="tab-main">
        <el-tabs type="border-card" style="height:811px">
            <el-tab-pane label="路由管理">
                <template>
                    <el-row :gutter="20">
                        <el-col :span="19">
                            <div>
                                <el-form :inline="true" class="demo-form-inline" method="post">
                                    <el-form-item label="菜单名称:">
                                        <el-input clearable v-model.trim="SelectRomeData.menuName"></el-input>
                                    </el-form-item>
                                    <el-form-item label="菜单级别:">
                                        <el-select v-model="SelectRomeData.menuLevel" clearable placeholder="请选择" style="width:150px;">
                                            <el-option
                                                v-for="item in SelectRomeData.menuOption"
                                                :key="item.value"
                                                :label="item.label"
                                                :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </el-form-item>
                                    <el-form-item label="归属系统:">
                                        <el-select v-model="SelectRomeData.sysType" clearable placeholder="请选择" style="width:150px;">
                                            <el-option
                                                v-for="item in SelectRomeData.sysTypeOption"
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
                                <el-table
                                    :data="tableData"
                                    height="596px"
                                    border
                                    >
                                    <el-table-column
                                        label="Index"
                                        type="index"
                                        align= "center"
                                        width="80px">
                                    </el-table-column>
                                    <el-table-column
                                        label="所属系统"
                                        align= "center"
                                        width="100px"
                                        prop="sysType">
                                    </el-table-column>  
                                    <el-table-column
                                        label="菜单级别"
                                        align= "center"
                                        width="100px"
                                        prop="levelText">
                                    </el-table-column>
                                    <el-table-column
                                        label="Index"
                                        align= "center"
                                        width="100px"
                                        prop="index">
                                    </el-table-column>
                                    <el-table-column
                                        label="菜单名称"
                                        width="300px"
                                        align= "center"
                                        prop="menuName">
                                    </el-table-column>
                                    <el-table-column
                                        label="路由地址"
                                        align= "center"
                                        prop="routerPath">
                                    </el-table-column>         
                                    <!-- <el-table-column
                                        label="所属上级ID"
                                        align= "center"
                                        width="100px"
                                        prop="belogId">
                                    </el-table-column>    -->
                                    <!-- <el-table-column
                                        label="排序"
                                        align= "center"
                                        width="100px"
                                        prop="sortNum">
                                    </el-table-column>   -->
                                    <el-table-column
                                        align="center"
                                        width="180px">
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
                                <el-pagination background layout="total, sizes, prev, pager, next, jumper"
                                    @size-change="pageSizeChange"
                                    @current-change="handleCurrentChange"
                                    :current-page="page.current" 
                                    :total="page.total"
                                    :page-sizes = [10,30,50,100]
                                    style="margin: 20px auto auto auto;">
                                </el-pagination>
                            </div>
                        </el-col>
                        <el-col :span="5">
                            <div style=" margin-top: 77px;">
                                <el-card style="height:595px">
                                    <el-tree
                                        :data="RightRomeData.TreeData"
                                        node-key="id"
                                        default-expand-all
                                        @node-drop="handleDrop"
                                        draggable
                                        :allow-drag="allowDrag"
                                        :allow-drop="allowDrop">
                                    </el-tree>
                                </el-card>
                            </div>
                        </el-col>
                    </el-row>
                </template>
            </el-tab-pane>
        </el-tabs>
        <!-- <template>
            <dialog-editor
                @closeDialog="closeDialog_Edit" 
                :isVisible="dialogVisible_editor" 
                :dialogPara="dialogPara_editor"
                @Succeed="SelectData">
            </dialog-editor>
        </template> -->
    </div>
</template>

<script>
import {PrintConsole} from "../../../js/Logger.js";
// import DialogEditor from "./Editor.vue";

export default {
    components: {
    //    DialogEditor,
    },
    data() {
        return {
            tableData:[],
            SelectRomeData:{
                menuName:'',
                menuLevel:'',
                menuOption:[
                    {'label':'一级菜单','value':'1'},
                    {'label':'二级菜单','value':'2'},
                ],
                sysType:'Home',
                sysTypeOption:[
                    {'label':'Home','value':'Home'},
                    {'label':'功能测试','value':'UI'},
                    {'label':'接口测试','value':'API'},
                    {'label':'性能测试','value':'PTS'},
                ],
            },
            RightRomeData:{
                TreeData:[],
                // TreeData:[
                //     {id: 1,label: '一级 1',children: [
                //         {id: 4,label: '二级 1-1'}
                //         ]
                //     }, 
                //     {id: 2,label: '一级 2',children: [
                //         {id: 5,label: '二级 2-1'},
                //         {id: 6,label: '二级 2-2'}
                //         ]
                //     }
                // ],
                defaultProps: {
                    children: 'children',
                    label: 'label'
                }
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
    mounted(){
        this.SelectData();
    },
    methods: {
        SelectData(){//刷新列表数据
            let self = this;
            self.tableData= [];
            self.$axios.get('/api/router/SelectData',{
                params:{
                    "menuName":self.SelectRomeData.menuName,
                    "menuLevel":self.SelectRomeData.menuLevel,
                    'sysType':self.SelectRomeData.sysType,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.levelText = d.levelText;
                        obj.index = d.index;
                        obj.menuName = d.menuName;
                        obj.routerPath = d.routerPath;
                        obj.sysType = d.sysType;

                        self.tableData.push(obj);
                    });
                    if(self.tableData.length==0 && self.page.current != 1){
                        self.page.current = 1;
                        self.SelectData();
                    }
                    self.page.total = res.data.Total;
                    self.GetPreviewData();
                }else{
                    self.$message.error(res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        // closeDialog_Edit(){
        //     this.dialogVisible_editor =false;
        // },
        // OpenEditDialog_Edit(){
        //     this.dialogPara_editor={
        //         dialogTitle:"新增路由",//初始化标题
        //         isAddNew:true,//初始化是否新增\修改
        //     }
        //     this.dialogVisible_editor=true;
        // },
        // handleEdit(index,row){
        //     this.dialogPara_editor={
        //         dialogTitle:"编辑路由",//初始化标题
        //         isAddNew:false,//初始化是否新增\修改
        //         routerId:row.id,
        //         level:row.level,
        //         index:row.index,
        //         menuName:row.menuName,
        //         routerPath:row.routerPath,
        //         belogId:row.belogId,
        //         sortNum:row.sortNum,
        //         toPage:row.toPage,
        //     }
        //     this.dialogVisible_editor=true;

        // },
        // handleDelete(index,row){
        //     this.$confirm('请确定是否删除?', '提示', {
        //         confirmButtonText: '确定',
        //         cancelButtonText: '取消',
        //         type: 'warning'
        //         }).then(() => {
        //             this.DataDelete(row.id);     
        //         }).catch(() => {       
        //     });
        // },
        // DataDelete(routerId){
        //     let self = this;
        //     self.$axios.post('/api/RouterManagement/DataDelete',{
        //         "data":{
        //             'routerId':routerId
        //         }
        //     }).then(res => {
        //     if(res.data.statusCode ==2003){
        //         self.$message.success('删除成功!');
        //         self.SelectData();
        //     }
        //     else{
        //         self.$message.error('删除失败:'+ res.data.errorMsg);
        //     }
        //     }).catch(function (error) {
        //         console.log(error);
        //     })
        // },
        GetPreviewData(){//加载预览数据
            let self = this;
            self.RightRomeData.TreeData= [];
            self.$axios.get('/api/router/GetPreviewData',{
                params:{
                    sysType:self.SelectRomeData.sysType,
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.RightRomeData.TreeData = res.data.TreeData;
                }else{
                    self.$message.error(res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        handleDrop(draggingNode, dropNode, dropType, ev) {//拖拽完成后的操作
            PrintConsole('tree drop: ', dropNode);
            PrintConsole('TreeData',this.RightRomeData.TreeData)
            let self = this;
            self.$axios.post('/api/RouterManagement/UpdateSort',{
                "data":{
                    'TreeData':self.RightRomeData.TreeData
                }
            }).then(res => {
            if(res.data.statusCode ==2002){
                self.$message.success('排序更新成功,请退出重新登录后应用!');
                self.SelectData();
            }
            else{
                self.$message.error('排序更新失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })

            
        },
        allowDrag(draggingNode){//判断节点能否被拖拽
            PrintConsole(draggingNode);
            if(draggingNode.data.allowDrag){//可拖动时
                return true
            }else{
                return false
            }
            // return draggingNode.data.label.indexOf('二级 2-1') === -1;//这个例子是不让这个可以拖动
        },
        allowDrop(draggingNode, dropNode, type) {//拖拽时判定目标节点能否被放置
            // console.log('tree drop: ', dropNode);
            // console.log('type:',type)
            if (dropNode.data.allowDrop === false) {
                return type !== 'inner';//这里我是没搞懂 但是功能能实现，vue官网上的例子
            } else {
                return true;
            }
        },
        ClearSelectRomeData(){
            let self=this;
            self.SelectRomeData.menuName='';
            self.SelectRomeData.menuLevel='';
            self.SelectRomeData.sysType='Home';
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


</style>
