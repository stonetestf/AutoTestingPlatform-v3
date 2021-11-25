<template>
    <div ref="tab-main"  id="tab-main">
        <el-tabs type="border-card" style="height:811px">
            <el-tab-pane label="操作信息">
                <template>
                    <el-form :inline="true" class="demo-form-inline" method="post">
                        <el-form-item label="所属系统:" prop="sysType">
                            <el-select v-model="SelectRomeData.sysType" clearable placeholder="请选择" style="width:150px;float:left;">
                                <el-option
                                    v-for="item in SelectRomeData.sysTypeOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <!-- <el-form-item label="事件名称:">
                            <el-input clearable v-model.trim="SelectRomeData.eventName"></el-input>
                        </el-form-item> -->
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </template>
                <template>
                    <el-table
                        :data="tableData"
                        height="596px"
                        border>
                        <el-table-column
                            label="Index"
                            align= "center"
                            width="80px"
                            type="index">
                        </el-table-column>
                        <el-table-column
                            label="所属系统"
                            width="100px"
                            align= "center"
                            prop="sysType">
                        </el-table-column>  
                        <el-table-column
                            label="所属页面"
                            width="150px"
                            align= "center"
                            prop="toPage">
                        </el-table-column>  
                        <el-table-column
                            label="所属功能"
                            width="200px"
                            align= "center"
                            prop="toFun">
                        </el-table-column>
                        <el-table-column
                            label="修改前"
                            align= "center"
                            prop="CUFront">
                        </el-table-column>
                        <el-table-column
                            label="修改后"
                            align= "center"
                            prop="CURear">
                        </el-table-column>
                        <el-table-column
                            label="操作时间"
                            width="200px"
                            align= "center"
                            prop="createTime">
                        </el-table-column>
                        <el-table-column
                            label="操作者"
                            align= "center"
                            width="100px"
                            prop="userName">
                        </el-table-column>
                    </el-table>
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
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import store from '../../../../store/index'

export default {
    components: {

    },
    data() {
        return {
            tableData:[],
            SelectRomeData:{
                sysType:'',
                sysTypeOption:[
                    {'label':'登录','value':'Login'},
                    {'label':'Home','value':'Home'},
                    {'label':'UI','value':'UI'},
                    {'label':'API','value':'API'},
                    {'label':'PTS','value':'PTS'},
                ],
            },
            page: { 
                current: 1,// 默认显示第几页
                total: 0,// 总条数，根据接口获取数据长度(注意：这里不能为空)
                pageSize: 10, // 默认每页显示的条数（可修改）
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
            self.$axios.get('/api/info/SelectOperationalInfo',{
                params:{
                    'sysType':self.SelectRomeData.sysType,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.sysType = d.sysType;
                        obj.toPage = d.toPage;
                        obj.toFun = d.toFun;
                        obj.CUFront = d.CUFront;
                        obj.CURear = d.CURear;
                        obj.createTime = d.createTime;
                        obj.userName = d.userName;

                        self.tableData.push(obj);
                    });
                    if(self.tableData.length==0 && self.page.current != 1){
                        self.page.current = 1;
                        self.SelectData();
                    }
                    self.page.total = res.data.Total;
                }else{
                    self.$message.error('操作信息获取失败:'+res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.sysType='';
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
            this.SelectData();
        },

    }
};
</script>

<style>


</style>
