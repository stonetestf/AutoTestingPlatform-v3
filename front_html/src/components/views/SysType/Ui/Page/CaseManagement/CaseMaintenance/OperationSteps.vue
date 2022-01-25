<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
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
                    
                </el-form>
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
                // this.ClearRomeData();

                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew;


                if(newval.isAddNew==false){//进入编辑状态
                    let self = this;

                }
            }
        },

    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },

    }
};
</script>

<style>
.test{
    text-align: left;
}
</style>
