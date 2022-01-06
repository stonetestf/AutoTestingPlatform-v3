<template>
  <div ref="tab-main"  id="tab-main">
    <template>
      <el-card class="MainCard">
          这个不能删除! 
          <span>这里放置:</span>
          <span>所有项目细致统计，该项目下有多少接口，单元测试，测试用例</span>
          <span>显示整个API系统的成功失败曲线或柱图</span>
          <span>显示整个API系统正在运行中的任务</span>
          <span>近10个失败次数最多的任务</span>
      </el-card>
    </template>
  </div>
</template>

<script>

// import * as echarts from 'echarts';
// import store from '../../../store/index'

export default {
  components: {

  },
  data() {
    return {
        RomeData:{
      

        },

    };
  },
  mounted(){


  },
  beforeDestroy(){//生命周期-离开时

  },
  methods: {
    
  }
};
</script>

<style>
.MainCard{
  height: 760px;
}

</style>
