<template>
     <div ref="tab-main"  id="tab-main" style="height:830px">
        <el-row>
            <el-col :span="4">
                <el-card class="btn" shadow="hover" @click.native="FromIntTest">
                    <el-image
                        style="width: 150px; height: 150px"
                        :src="IconImg.api"
                        fit="cover">
                    </el-image>
                    <div class="btn-text">接口测试(开发中)</div>
                </el-card>
            </el-col>
            <el-col :span="4">
                <el-card class="btn" shadow="hover" @click.native="FromFunTest">
                    <el-image
                        style="width: 150px; height: 150px"
                        :src="IconImg.ui"
                        fit="cover">
                    </el-image>
                    <div class="btn-text">功能测试(建设中)</div>
                </el-card>
            </el-col>
            <el-col :span="4">
                <el-card class="btn" shadow="hover" @click.native="FromPerTest">
                    <el-image
                        style="width: 150px; height: 150px"
                        :src="IconImg.pts"
                        fit="cover">
                    </el-image>
                    <div class="btn-text">性能测试(建设中)</div>
                </el-card>
            </el-col>
            <!-- <el-col :span="5">
                
            </el-col>
            <el-col :span="5">
            </el-col> -->
        </el-row>
     </div>
</template>
<script>

import api from '@/assets/images/Choose/API.png'
import ui from '@/assets/images/Choose/UI.png'
import pts from '@/assets/images/Choose/PTS.png'


  export default {
    data() {
      return {
        IconImg:{
            api:api,
            ui:ui,
            pts:pts,
        },
        //   TimedTask
      };
    },
    mounted(){

    },
    methods: {
        // FromIntTest(){
        //     // this.$router.push('/Home_int');
        //     this.$router.push({ path:'/TestType_Int/Home'});
        // },
        // FromFunTest(){
        //     // this.$router.push('/Home_fun');
        //     this.$router.push({ path:'/TestType_Fun/Home'});
        // },
        // FromPerTest(){
        //     this.$router.push({ path:'/TestType_Per/Home'});
        // }

    }
  };
</script>

<style>
    /* .box-card{
        height:811px;
    } */
    .btn-text{
        font-size: 30px;
    }
    .btn{
        height: 250px;
        width: 250px;
    }
    .btn-div{
       margin-top: 15%;
    }
</style>
