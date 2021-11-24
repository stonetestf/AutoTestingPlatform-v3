import Vue from 'vue'

// Vue.prototype.$axios;

// 获取项目名称下拉列表
function GetRoleNameItems(){
    return Vue.prototype.$axios.get('/api/role/GetRoleNameItems',{
        params:{
            // 'data':{}
        }
    }).then(res => {
        if(res.data.statusCode == 2000){
            // console.log(res.data.itemsData)
            return res.data.itemsData;
        }
    }).catch(function (error) {
        console.log(error);
    })
}


export {
    GetRoleNameItems
  };
  