<template>
    <el-drawer
    :title="dialogTitle"
    size="750px"
    :wrapperClosable="false"
    :visible.sync="dialogVisible"
    direction='rtl'
    :before-close="dialogClose">
      <el-card style="height:860px">
        <template>
            <div class="table"
                v-loading="loading"
                element-loading-text="拼命加载中"
                element-loading-spinner="el-icon-loading">
                <div class="father" style="width: 100%; height: 600px;">
                    <div class="son" style="width: 650px; height: 450px;">
                        <!-- <el-card style="width:700px" shadow="never"> -->
                            <el-form ref="RomeData" :inline="true" :rules="rules" :model="RomeData"  label-width="100px">
                                <el-form-item label="工单类型:" prop="workType">
                                    <el-select v-model="RomeData.workType" clearable placeholder="请选择" style="width:200px;float:left;">
                                        <el-option
                                            v-for="item in RomeData.workTypeNameOption"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="工单状态:" prop="workState">
                                    <el-select v-model="RomeData.workState" clearable placeholder="请选择" style="width:200px;float:left;">
                                        <el-option
                                            v-for="item in RomeData.workStateNameOption"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="所属页面:" prop="pageId">
                                    <el-select v-model="RomeData.pageId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetPageNameOption()">
                                        <el-option
                                            v-for="item in RomeData.pageNameOption"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="所属功能:" prop="funId">
                                    <el-select v-model="RomeData.funId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetFunNameOption()">
                                        <el-option
                                            v-for="item in RomeData.funNameOption"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="工单名称:" prop="workName">
                                    <el-input v-model.trim="RomeData.workName" style="width:515px"></el-input>
                                </el-form-item>
                                <div>
                                    <el-form-item label="工单信息:">
                                        <el-input type="textarea" 
                                        :autosize="{ minRows: 10, maxRows: 10}"
                                        v-model="RomeData.workMessage"
                                         style="width:515px"></el-input>
                                    </el-form-item>
                                </div>
                                <el-form-item label="推送To:">
                                    <el-cascader 
                                        @click.native="GetUserNameOption()"
                                        style="width:515px"
                                        v-model="RomeData.pushTo" 
                                        :options="RomeData.userNameOptions" 
                                        :props="RomeData.props" 
                                        :show-all-levels="false" 
                                        clearable>
                                        <template slot-scope="{ node, data }">
                                            <span>{{ data.label }}</span>
                                            <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                        </template>
                                    </el-cascader>
                                </el-form-item>
                                <div>
                                    <el-button type="primary" @click="submitForm('RomeData')">确定</el-button>
                                    <el-button @click="ClearRomeData()">重置</el-button>
                                </div>
                            </el-form>
                        <!-- </el-card> -->
                    </div>
                </div>
            </div>
        </template>
      </el-card>
    </el-drawer>
</template>

<script>
import Qs from 'qs'
import {PrintConsole} from "../../../js/Logger.js";
import {GetPageNameItems} from "../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../js/GetSelectTable.js";
import {GetUserNameItems} from "../../../js/GetSelectTable.js";

export default {
    components: {
       
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            RomeData:{
                workId:'',
                workType:'',
                workTypeNameOption:[
                    {'label':'新增','value':'Add'},
                    {'label':'修改','value':'Edit'},
                    {'label':'删除','value':'Delete'},
                    {'label':'其他','value':'Other'},
                ],
                workState:'',
                workStateNameOption:[
                    {'label':'待受理','value':0},
                    {'label':'受理中','value':1},
                    {'label':'已解决','value':2},
                ],
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                workName:'',
                workMessage:'',
                props: { multiple: true },
                pushTo:[],
                userNameOptions:[],
            },
            rules:{
                workType:[{required: true, message: '请选择工单类型', trigger: 'change' }],
                workState:[{required: true, message: '请选择工单状态', trigger: 'change' }],
                pageId:[{required: true, message: '请选择所属页面', trigger: 'change' }],
                funId:[{required: true, message: '请选择所属功能', trigger: 'change' }],
                workName: [
                    { required: true, message: '请输入工单名称', trigger: 'blur' },
                    { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                ],
            },
        };
    },
    mounted(){
  
    },
    computed:{//计算属性
      
    },
    props:[//main页面在引用editor时 必须声明所需要调用的属性
        'isVisible','dialogPara'
    ],
    watch:{//当我们输入值后，wacth监听每次修改变化的新值，然后计算输出值
        isVisible:{//用于监听父页面的isVisible，true时就弹出窗口
            handler(newval,oldval)
            {
                this.dialogVisible=newval;  
            }
        },
        dialogPara:{
            handler(newval,oldval)
            {
                PrintConsole(newval);
                this.ClearRomeData();
                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew

                if(newval.isAddNew==false){//进入编辑状态
                    let self = this;
                    self.RomeData.workId=newval.workId;
                    self.LoadEditData(newval.workId).then(d=>{
                        if(d.statusCode==2000){
                            self.RomeData.workType = d.dataTabel.workType;
                            self.RomeData.workState = d.dataTabel.workState;
                            GetPageNameItems(this.$cookies.get('proId')).then(dd=>{
                                self.RomeData.pageNameOption = dd;
                                self.RomeData.pageId = d.dataTabel.pageId;
                                GetFunNameItems(this.$cookies.get('proId'),this.RomeData.pageId).then(dd=>{
                                    self.RomeData.funNameOption = dd;
                                    self.RomeData.funId = d.dataTabel.funId;
                                    self.RomeData.workName = d.dataTabel.workName;
                                    self.RomeData.workMessage = d.dataTabel.workMessage;
                                    GetUserNameItems().then(dd=>{
                                        self.RomeData.userNameOptions = dd;
                                        self.RomeData.pushTo = d.dataTabel.pushTo;
                                    });
                                });
                            });
                        }else{
                            self.$message.error('获取数据失败:'+d.errorMsg);
                        }
                    });
                }
            }
        },
        'RomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.RomeData.funId='';
                self.RomeData.funNameOption=[];
            }
        },
     
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        ClearRomeData(){
            let self = this;
            self.resetForm('RomeData');
            self.RomeData.workType='';
            self.RomeData.workState='';
            self.RomeData.pageId='';
            self.RomeData.funId='';
            self.RomeData.workName='';
            self.RomeData.workMessage='';
            self.RomeData.pushTo=[];
        },
        GetPageNameOption(){
            GetPageNameItems(this.$cookies.get('proId')).then(d=>{
                this.RomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            if(this.RomeData.pageId){
                GetFunNameItems(this.$cookies.get('proId'),this.RomeData.pageId).then(d=>{
                    this.RomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        GetUserNameOption(){
            GetUserNameItems().then(d=>{
                this.RomeData.userNameOptions = d;
            });
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        SaveData(){
            let self = this;
            if(self.isAddNew){
                self.$axios.post('/api/WorkorderManagement/SaveData',Qs.stringify({
                    'sysType':'API',
                    'proId':self.$cookies.get('proId'),
                    'pageId':self.RomeData.pageId,
                    'funId':self.RomeData.funId,
                    'workType':self.RomeData.workType,
                    'workState':self.RomeData.workState,
                    'workName':self.RomeData.workName,
                    'workMessage':self.RomeData.workMessage,
                    'pushTo':self.RomeData.pushTo.toString(),
                })).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('新增工单成功');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('新增工单失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/WorkorderManagement/EditData',Qs.stringify({
                    'workId':self.RomeData.workId,
                    'sysType':'API',
                    'proId':self.$cookies.get('proId'),
                    'pageId':self.RomeData.pageId,
                    'funId':self.RomeData.funId,
                    'workType':self.RomeData.workType,
                    'workState':self.RomeData.workState,
                    'workName':self.RomeData.workName,
                    'workMessage':self.RomeData.workMessage,
                    'pushTo':self.RomeData.pushTo.toString(),
                })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('修改工单成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('修改工单失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }
        },
        LoadEditData(workId){
            let self = this;
            self.loading=true;
            return self.$axios.get('/api/WorkorderManagement/LoadData',{
                params:{
                    'workId':workId
                }
            }).then(res => {
                self.loading=false;
                return res.data
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
        },
        submitForm(formName) {//保存
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.SaveData();
                } 
            });
        },

    }
};
</script>

<style>
.table {display: table; width: 100%;}
.father {display: table-cell; vertical-align: middle;}
.son {margin: auto;}
</style>
