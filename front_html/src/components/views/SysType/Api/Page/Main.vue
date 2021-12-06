<template>
  <div ref="tab-main"  id="tab-main">
    <template>
      <el-card class="MainCard">
          <span>这里显示当前项目的接口数量，单元测试数量，测试用例数量，定时任务数据，批量任务数量</span>
          <span>当前项目的成功，失败全统计</span>
          <span>当前项目10个失败数量最多的任务</span>
           <span>当前项目的任务队列</span>
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
  height: 750px;
}

</style>
