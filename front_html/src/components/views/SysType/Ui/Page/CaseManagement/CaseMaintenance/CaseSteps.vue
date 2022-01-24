<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :close-on-press-escape="false"
            :before-close="dialogClose">
            <div
                v-loading="loading"
                element-loading-text="拼命加载中"
                element-loading-spinner="el-icon-loading">
                <el-divider content-position="center">事件操作</el-divider>
                <div>
                    <el-form ref="RomeData" :model="RomeData" :rules="RomeData.rules" label-width="100px">
                        <el-form-item label="事件名称:"  prop="eventName">
                            <el-input v-model="RomeData.eventName" clearable placeholder="请输入事件名称,为空时取元素名称" style="width:300px;float:left"></el-input>
                        </el-form-item>
                        <!-- <el-form-item label="用例标签:">
                            <el-select v-model="RomeData.caselabelId" clearable multiple placeholder="请选择" style="width:300px;float:left" @click.native="GetCaseLabelNameOption()">
                                <el-option
                                v-for="item in tRomeData.caselabeNameOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item> -->
                        <div v-if="DisPlay.element">
                            <el-divider content-position="center">元素操作</el-divider>
                            <el-form-item label="选择元素:" prop="elementId">
                                <el-select 
                                    v-model="RomeData.elementId" 
                                    filterable clearable placeholder="请选择" 
                                    style="width:300px;float:left" 
                                    @change="handleChange_elementId"
                                    @click.native="GeElementNameOption()">
                                    <el-option
                                        v-for="item in RomeData.elementNameOption"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </div>
                        <el-form-item label="元素类型:" prop="elementType">
                            <el-cascader
                                @click.native="GetElementOperationType()"
                                clearable
                                v-model="RomeData.elementType"
                                :options="RomeData.elementTypeOptions"
                                style="width:300px;float:left">
                                <template slot-scope="{ node, data }">
                                    <span>{{ data.label }}</span>
                                    <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                </template>
                            </el-cascader>
                        </el-form-item>
                        <div v-if="DisPlay.inputData">
                            <el-form-item label="输入/选择:">
                            <div v-if="RomeData.operationType[1]=='Upload'">
                                <!-- <el-upload 
                                    :headers="headers"
                                    :action="RomeData.uploadToTemp"
                                    :on-success="upload_success"
                                    :on-remove="upload_remove"
                                    :limit="1"
                                    :file-list="RomeData.fileList">
                                    <el-button size="small" type="primary">点击上传</el-button>
                                </el-upload> -->
                            </div>
                            <div v-else>
                                <el-input v-model="RomeData.inputData" clearable style="width:300px;float:left"></el-input>
                            </div>
                            </el-form-item>
                        </div>
                        <div v-if="DisPlay.assert">
                            <el-divider content-position="center">断言操作</el-divider>
                            <el-form-item label="断言类型:" prop="assertType">
                                <el-select v-model="RomeData.assertType" placeholder="请选择" style="width:300px;float:left">
                                    <el-option
                                    v-for="item in RomeData.assertTypeOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="断言值类型:" prop="assertDataTypeId">
                                <el-select v-model="RomeData.assertValueType" placeholder="请选择" style="width:300px;float:left">
                                    <el-option
                                        v-for="item in RomeData.assertValueTypeOption"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="断言值:">
                                <el-input v-model="RomeData.assertValue" clearable placeholder="请输入断言值" style="width:300px;float:left"></el-input>
                            </el-form-item>
                        </div>
                        <div v-if="DisPlay.imageOperation">
                            <el-divider >图片操作</el-divider>
                            <!-- <el-form-item label="选择图片:" prop="pictureContrast">
                                <el-cascader
                                    style="width:300px"
                                    :props="{ multiple: true }"
                                    clearable
                                    v-model="RomeData.pictureContrast" placeholder="请选择"
                                    :options="RomeData.pictureContrastNameOption"
                                    @click.native="LoadContrastImgList()"
                                    @change="handleChange_pictureContrast">
                                    <template slot-scope="{ node, data }">
                                        <span>{{ data.label }}</span>
                                        <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                    </template>
                                </el-cascader>
                            </el-form-item>
                            <el-form-item label="对比类型:" prop="contrastTypeId" v-if="RomeData.disPlay.contrastType">
                                <el-select 
                                v-model="RomeData.contrastTypeId"  
                                placeholder="请选择" 
                                @click.native="LoadContrastType()"
                                style="width:300px;float:left">
                                    <el-option
                                        v-for="item in RomeData.contrastTypeNameOption"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item> -->
                        </div>
                    </el-form>
                </div>
                <div>
                    <el-button v-if="RomeData.currentEventType=='Add'" type="primary" @click="submitForm_CaseSortRomeData()">新增</el-button>
                    <el-button v-else type="warning" @click="EditCaseToTable()">保存</el-button>
                    <el-button @click="ClearCaseSortRomeData('reset')">重置</el-button>
                </div>
                <el-divider >操作提示</el-divider>
                <div class="operationTips">
                    <div 
                    v-for="item in RomeData.operationTips"
                    :key="item"
                    >{{item}}</div>
                </div>
            </div>
            </el-drawer>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";

import {GetElementOperationTypeItems} from "../../../../../../js/GetSelectTable.js";

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
                eventName:'',
                elementId:'',
                elementNameOption:[],
                elementType:'',
                elementTypeOptions:[],
                inputData:'',
                assertType:'',
                assertTypeOption:[
                    {'label':'等于(Equals)','value':'Equals'},
                    {'label':'不等于(NotEquals)','value':'NotEquals'},
                    {'label':'包含(Contains)','value':'Contains'},
                ],
                assertValueType:'',
                assertValueTypeOption:[
                    {'label':'Str','value':'Str'},
                    {'label':'List','value':'List'},
                    {'label':'Dict','value':'Dict'},
                    {'label':'Int','value':'Int'},
                    {'label':'Float','value':'Float'},
                ],
                assertValue:'',



            },
            DisPlay:{
                element:true,
                inputData:false,
                assert:false,
                imageOperation:false,
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

                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew;

                if(newval.isAddNew==false){//进入编辑状态
        
                  
                }
            }
        },

    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        GetElementOperationType(){
            GetElementOperationTypeItems().then(d=>{
                if(d.statusCode==2000){
                    this.RomeData.elementTypeOptions = d.dataList;
                }else{
                    self.$message.errorMsg('列表数据获取失败:'+d.errorMsg);
                }
            });
        },
    }
};
</script>

<style>

</style>
