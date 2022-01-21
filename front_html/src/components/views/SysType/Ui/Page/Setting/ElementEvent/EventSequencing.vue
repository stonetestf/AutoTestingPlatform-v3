<template>
    <el-drawer
        :title="dialogTitle"
        size="400px"
        :wrapperClosable="false"
        :visible.sync="dialogVisible"
        direction='rtl'
        :before-close="dialogClose">
            <el-tree
                :data="RomeData.TreeData"
                node-key="id"
                default-expand-all
                @node-drop="handleDrop"
                draggable
                :allow-drag="allowDrag"
                :allow-drop="allowDrop">
            </el-tree>
    </el-drawer>
</template>

<script>
import Qs from 'qs'
import {PrintConsole} from "../../../../../../js/Logger.js";

export default {
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            RomeData:{
                TreeData:[]
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
                PrintConsole(newval);


                this.dialogTitle = newval.dialogTitle;

            }
        },
     
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
            this.$emit('Succeed');//回调查询
        },
    }
};
</script>

<style>

</style>
