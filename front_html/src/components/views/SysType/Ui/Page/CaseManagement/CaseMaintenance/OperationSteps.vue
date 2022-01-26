<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="450px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :before-close="dialogClose">
            <div style="text-align: left;">
                <el-form ref="RomeData" :inline="true" :rules="RomeData.rules" :model="RomeData"  label-width="100px">
                    <el-form-item prop="location" label="操作位置:">
                        <el-select v-model="RomeData.location" clearable placeholder="请选择操作位置" style="width:150px;float:left;" >
                            <el-option
                                v-for="item in RomeData.locationOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item prop="operationType" label="操作类型:">
                        <el-select v-model="RomeData.operationType" clearable placeholder="请选择操作位置" style="width:300px;float:left;" >
                            <el-option
                                v-for="item in RomeData.operationTypeOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="选择用例:" v-if="RomeData.operationType=='TestCase'">
                        <el-select v-model="RomeData.caseId" clearable placeholder="请选择需要运行的用例" style="width:300px;float:left;" >
                            <el-option
                                v-for="item in RomeData.caseNameOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="输入方法:" v-else-if="RomeData.operationType=='Methods'">
                        <el-input v-model="RomeData.methodsName" clearable placeholder="输入方法函数名称" style="width:300px;float:left;"></el-input>
                    </el-form-item>
                    <el-form-item label="选择DB:" v-else-if="RomeData.operationType=='DataBase'">
                        <el-cascader
                            style="float:left;width:300px;"
                            clearable
                            placeholder="请选择连接的数据库" 
                            v-model="RomeData.dataBase"
                            :options="RomeData.dataBaseOptions"
                            @click.native="getDataBaseOption()">
                            <template slot-scope="{ node, data }">
                                <span>{{ data.label }}</span>
                                <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                            </template>
                        </el-cascader>
                    </el-form-item>
                    <el-form-item label="备注:">
                            <el-input  
                                style="width:300px"
                                type="textarea"
                                :autosize="{ minRows: 6, maxRows: 6}"
                                placeholder="请输入内容"
                                v-model="RomeData.remarks"></el-input>
                    </el-form-item>
                </el-form>
            </div>
            <div>
                <el-button type="success" @click="AddToOperationTable()" v-if="isAddNew">保存</el-button>
                <el-button type="warning" @click="EditToOperationTable()" v-else>修改</el-button>
                <el-button @click="ClearRomeData('reset')">重置</el-button>  
            </div>
            </el-drawer>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";

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
                id:'',
                location:'',//位置
                locationOption:[
                    {'label':'前置操作','value':'Pre'},
                    {'label':'后置操作','value':'Rear'},
                ],
                operationType:'',
                operationTypeOption:[
                    {'label':'测试用例','value':'TestCase'},
                    {'label':'方法函数','value':'Methods'},
                    {'label':'数据库操作','value':'DataBase'},
                ],
                caseId:'',
                caseNameOption:[],
                methodsName:'',
                dataBase:'',
                dataBaseOptions:[],
                remarks:'',
                rules:{
                    location:[{ required: true, message: '请选择操作位置', trigger: 'change' }],
                    operationType:[{ required: true, message: '请选择操作类型', trigger: 'change' }],
                }
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
                this.isAddNew = newval.isAddNew;
                this.RomeData.id=newval.id;

                if(newval.isAddNew==false){//进入编辑状态
                    let self = this;

                }
            }
        },
        'RomeData.operationType': function (newVal,oldVal) {//选择元素后加载当前这个元素的元素类型
            if(newVal!=oldVal){
                PrintConsole(newVal);
            }
        },

    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                PrintConsole('清除正则验证')
                this.$refs[formName].resetFields();
            }
        },
        ClearRomeData(){
            let self = this;
            self.resetForm('RomeData');
            self.RomeData.location='';
            self.RomeData.operationType='';
            self.RomeData.caseId='';
            self.RomeData.methodsName='';
            self.RomeData.dataBase='';
            self.RomeData.remarks='';
        },
        AddToOperationTable(){
            let self = this;
            let obj = {};
            obj.state = true;
            obj.id=self.RomeData.id;
            obj.location = self.RomeData.location;
            obj.operationType = self.RomeData.operationType;
            obj.caseId = self.RomeData.caseId;
            obj.methodsName = self.RomeData.methodsName;
            obj.dataBase = self.RomeData.dataBase;
            obj.remarks = self.RomeData.remarks;

            self.$emit('geAddtData',obj);//回调传值
            self.dialogClose();
        },
        EditToOperationTable(){
            let self = this;
            self.$emit('geEditData',);//回调传值
        },

    }
};
</script>

<style>
.test{
    text-align: left;
}
</style>
