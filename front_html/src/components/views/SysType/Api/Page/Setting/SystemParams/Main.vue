<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <el-card class="MainCard">
                <template>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="参数名称:">
                            <el-input clearable v-model.trim="SelectRomeData.paramsName"></el-input>
                        </el-form-item>
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </template>
                <template>
                    <div>
                        <el-table
                            :data="tableData"
                            height="619px"
                            border>
                            <el-table-column
                                label="ID"
                                align= "center"
                                width="100px"
                                prop="id">
                            </el-table-column>
                            <el-table-column
                                label="参数名称"
                                align= "center"
                                prop="paramsName">
                            </el-table-column>
                            <el-table-column
                                label="参数类型"
                                width="150px"
                                align= "center"
                                prop="paramsType">
                            </el-table-column>
                            <el-table-column
                                label="参数值"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-input v-if="scope.row.whetherValue" v-model.trim="RomeData.paramsValue"></el-input>
                                    <span v-else>{{scope.row.paramsValue}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="备注"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-input v-if="scope.row.whetherRemarks" v-model="RomeData.remarks"></el-input>
                                    <span v-else>{{scope.row.remarks}}</span>
                                </template>
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
                                label="操作"
                                align="center"
                                width="100px">
                            <template slot-scope="scope" style="width:100px">
                                <el-button
                                    v-if="scope.row.whetherSave"
                                    size="mini"
                                    type="primary"
                                    @click="handleSave(scope.$index,scope.row)">Save</el-button>
                                <el-button
                                    v-else
                                    size="mini"
                                    @click="handleEdit(scope.$index,scope.row)">Edit</el-button>
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
    </div>
</template>

<script>

export default {
    components: {
    },
    data() {
        return {
            tableData: [
                {}
            ],
            SelectRomeData:{
                paramsName:'',
            },
            RomeData:{
                paramsName:'',
                paramsValue:'',
                remarks:'',
                whetherEdit:false,
                whetherRemarks:false,
    
            },
            page: { 
                current: 1,// 默认显示第几页
                total: 0,// 总条数，根据接口获取数据长度(注意：这里不能为空)
                pageSize: 10, // 默认每页显示的条数（可修改）
            },
        };
    },
    mounted(){
        // this.SelectData();
    },
    methods: {
        SelectData(){//刷新列表数据
            let self = this;
            self.tableData= [];
            self.$axios.get('/api/Int_GlobalParams/SelectData',{
                params:{
                    'data':{
                        'paramsName':self.SelectRomeData.paramsName,
                        'current':self.page.current,
                        'pageSize':self.page.pageSize
                    }
                }
            }).then(res => {
                res.data.TableData.forEach(d => {
                    let obj = {};
                    obj.id =d.id;
                    obj.paramsName = d.paramsName;
                    obj.whetherValue = false;
                    obj.paramsValue = d.paramsValue;
                    obj.whetherRemarks = false;
                    obj.remarks = d.remarks;
                    obj.updateTime = d.updateTime;
                    obj.userName = d.userName;
                    obj.whetherSave = false;

                    self.tableData.push(obj);
                });
                if(self.tableData.length==0 && self.page.current != 1){
                    self.page.current = 1;
                    self.SelectData();
                }
                self.page.total = res.data.Total;
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
            })
        },
        handleEdit(index,row){
            console.log('row',row)
            let self = this;
            if(self.RomeData.whetherEdit){
                self.$message.warning('请完成:'+row.paramsName +',的设置的编辑后在进后其他操作！');
            }else{
                self.RomeData.whetherEdit = true;
                // self.RomeData.id = row.id;
                self.tableData[index].whetherValue=true;
                self.RomeData.paramsValue = row.paramsValue;
                self.tableData[index].whetherRemarks=true;
                self.RomeData.remarks = row.remarks;

                self.tableData[index].whetherSave=true;
            }
        },
        handleSave(index,row){
            let self = this;
            self.tableData[index].whetherValue=false;
            self.tableData[index].whetherSave=false;
            self.tableData[index].whetherRemarks=false;
            self.$axios.post('/api/Int_GlobalParams/DataEdit',{
                "userId":store.state.userId,
                "data":{
                    'paramsId':row.id,
                    'paramsValue':self.RomeData.paramsValue,
                    'remarks':self.RomeData.remarks
                    }
            }).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('全局参数修改完成!');
                    self.SelectData();
                }
                else{
                    self.$message.error('全局参数修改失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
            })
            self.RomeData.whetherEdit = false; 
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.paramsName='';
            self.RomeData.whetherEdit = false;

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
