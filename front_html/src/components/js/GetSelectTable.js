import Vue from 'vue'

// Vue.prototype.$axios;

//API
// 获取项目名称下拉列表-无Token版本
function NoTokenGetRoleNameItems(){
    return Vue.prototype.$axios.get('/api/role/NoTokenGetRoleNameItems',{
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

function GetPageNameItems(proId){
    return Vue.prototype.$axios.get('/api/PageManagement/GetPageNameItems',{
        params:{
            'proId':proId,
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

function GetFunNameItems(proId,pageId){
    return Vue.prototype.$axios.get('/api/FunManagement/GetFunNameItems',{
        params:{
            'proId':proId,
            'pageId':pageId,
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

function GetPageEnvironmentNameItems(proId){
    return Vue.prototype.$axios.get('/api/PageEnvironment/GetPageEnvironmentNameItems',{
        params:{
            'proId':proId,
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

function GetUserNameItems(){
    return Vue.prototype.$axios.get('/api/userManagement/GetUserNameItems',{
        params:{
  
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

//加载数据库环境的IP及以下可用的库名
function GetConnectBaseItems(sysType){
    return Vue.prototype.$axios.get('/api/DataBaseEnvironment/GetConnectBaseItems',{
        params:{
            'sysType':sysType
        }
    }).then(res => {
        return res.data;
    }).catch(function (error) {
        console.log(error);
    })
}

//UI
//加载元素的操作类型
function GetElementOperationTypeItems(){
    return Vue.prototype.$axios.get('/api/UiElementEvent/GetElementOperationTypeItems',{
        params:{
            
        }
    }).then(res => {
        return res.data;
    }).catch(function (error) {
        console.log(error);
    })
}

//加载元素
function GeElementNameItems(pageIdList){
    return Vue.prototype.$axios.get('/api/UiElementMaintenance/GeElementNameItems',{
        params:{
            'pageIdList':pageIdList
        }
    }).then(res => {
        return res.data;
    }).catch(function (error) {
        console.log(error);
    })
}

export {
    NoTokenGetRoleNameItems,GetRoleNameItems,GetPageNameItems,GetFunNameItems,GetUserNameItems,GetPageEnvironmentNameItems,GetConnectBaseItems,

    GetElementOperationTypeItems,GeElementNameItems
  };
  