<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="1200px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :before-close="dialogClose">
                <el-steps :active="StepsRomeData.active" simple :process-status="StepsRomeData.processStatus" finish-status="success">
                    <el-step title="维护基本信息"></el-step>
                    <el-step title="编写接口信息"></el-step>
                    <el-step title="效验接口参数"></el-step>
                </el-steps>
                <el-card style="height:755px"
                    v-loading="loading"
                    element-loading-text="拼命加载中"
                    element-loading-spinner="el-icon-loading">
                    <template v-if="StepsRomeData.active==0">
                        <div class="table">
                            <div class="father" style="width: 100%; height: 550px;">
                                <div class="son" style="width:1100px; height: 150px;">
                                    <div style="margin-top:20px;">
                                        <el-card shadow="never">
                                            <el-form ref="ApiRomeData" :inline="true" :rules="ApiRomeData.rules" :model="ApiRomeData"  label-width="100px">
                                                <el-form-item label="所属页面:" prop="pageId">
                                                    <el-select v-model="ApiRomeData.pageId" clearable placeholder="请选择" @click.native="GetProNameOption()">
                                                        <el-option
                                                            v-for="item in ApiRomeData.pageNameOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="所属功能:" prop="funId">
                                                    <el-select v-model="ApiRomeData.funId" clearable placeholder="请选择" @click.native="GetProNameOption()">
                                                        <el-option
                                                            v-for="item in ApiRomeData.funNameOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="页面环境:" prop="environmentId">
                                                    <el-select v-model="ApiRomeData.environmentId" clearable placeholder="请选择" @click.native="GetProNameOption()">
                                                        <el-option
                                                            v-for="item in ApiRomeData.environmentNameOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="接口名称:" prop="apiName">
                                                    <el-input placeholder="请输入接口名称" v-model="ApiRomeData.apiName" style="width:550px;"></el-input>
                                                </el-form-item>
                                                <el-form-item label="接口状态:" prop="apiState">
                                                    <el-select v-model="ApiRomeData.apiState" clearable placeholder="请选择" >
                                                        <el-option
                                                            v-for="item in ApiRomeData.apiStateOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                            </el-form>
                                        </el-card>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==1">

                    </template>
                    <template v-else>
                    </template>
                </el-card>
                <el-button style="margin-top: 12px;" icon="el-icon-arrow-left" type="primary" v-if="StepsRomeData.disPlay_Previous" @click="previous">上一步</el-button>
                <el-button style="margin-top: 12px;" type="primary" v-if="StepsRomeData.disPlay_Next" @click="next">下一步<i class="el-icon-arrow-right el-icon--right"></i></el-button>
                <el-button style="margin-top: 12px;" type="success" v-if="StepsRomeData.disPlay_Save" @click="returnToMain()">保存</el-button>
            </el-drawer>
        </template>
    </div>
</template>

<script>


export default {
    components: {
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            StepsRomeData:{
                active:0,
                stepLength:2,//步长，整个窗口可以执行的步骤数
                processStatus:'process',
                disPlay_Save:false,
                disPlay_Next:true,
                disPlay_Previous:false,
            },
            ApiRomeData:{
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                environmentId:'',//页面环境
                environmentNameOption:[],
                apiName:'',
                apiState:'',
                apiStateOption:[
                    {'label':'启用','value':'0'},
                    {'label':'禁用','value':'1'},
                ],
                rules:{

                },
            }
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
                console.log(newval);
                this.ClearStepsRomeData();
                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew

                if(newval.isAddNew==false){//进入编辑状态
                
                }
            }
        },
        'StepsRomeData.active': function (newVal,oldVal) {//监听步骤
            // console.log('newVal:'+newVal)
            let self = this;
            if(newVal==0){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = false;
               
            }else if(newVal==1){
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = true;
                self.StepsRomeData.disPlay_Save = false;
            }else{
                self.StepsRomeData.disPlay_Save = true;
                self.StepsRomeData.disPlay_Next = false;
                self.StepsRomeData.disPlay_Previous = true;
            }
            console.log('步骤',this.StepsRomeData.active)
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        //导航条事件
        next() {//下一步
            let self = this;
            console.log('当前',self.StepsRomeData.active)
            if(self.StepsRomeData.active==0){//基本用例数据
                self.StepsRomeData.active++;
                // this.$refs['BasicRomeData'].validate((valid) => {
                //     if (valid) {//通过
                //         self.StepsRomeData.active++;
                //     } 
                // });
            }else if(self.StepsRomeData.active==1){
                self.StepsRomeData.active++;
            }
        },
        previous(){//上一步
            let self = this;
            self.StepsRomeData.processStatus='process';
            if(self.StepsRomeData.active==0){

            }else if(self.StepsRomeData.active==3){
                self.StepsRomeData.active--;
                self.StepsRomeData.active--;
            }
            else{
                self.StepsRomeData.active--;
            }
            console.log('步骤',this.StepsRomeData.active)
        },
        ClearStepsRomeData(){
            let self = this;
            // self.resetForm('RomeData');
            self.StepsRomeData.active= 0;
            self.StepsRomeData.disPlay_Save = false;
            self.StepsRomeData.disPlay_Next = true;
            self.StepsRomeData.processStatus ='process';
        },
        returnToMain(){
            let self = this;
            self.dialogVisible = false;//关闭新增弹窗
            self.$emit('closeDialog');
            self.$emit('Succeed');//回调查询   
        },
    }
};
</script>

<style>
.table {display: table; width: 100%;}
.father {display: table-cell; vertical-align: middle;}
.son {margin: auto;}

</style>
