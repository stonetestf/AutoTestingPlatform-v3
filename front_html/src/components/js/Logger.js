import store from '../../store/index'

// 打印log
function PrintConsole(info){
    if(store.state.isDebug){
        console.log(info);
    }
  
}


export {
    PrintConsole
  };
  