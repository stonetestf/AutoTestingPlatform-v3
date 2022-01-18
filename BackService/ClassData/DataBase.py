import MySQLdb

# Create reference here.
from ClassData.Logger import Logging as cls_Logging
from ClassData.Common import Common as cls_Common


# Create info here.

class DataBase(cls_Logging, cls_Common):
    def connect_test(self,dbType,dataBaseIp, port, userName, passWord):
        results = {}
        if dbType == "MySql":
            results = self.connect_mysql(dataBaseIp, port, userName, passWord)
        return results

    def connect_mysql(self,ip,port,user,pwd):
        results = {}
        dataBaseList = []
        try:
            conn = MySQLdb.connect(
                host=ip,
                port=int(port),
                user=user,
                passwd=pwd,
            )
            cur = conn.cursor()
            cur.execute('show databases')
            for i in range(cur.rowcount):
                row = cur.fetchone()
                dataBaseList.append(row[0])
            cur.close()
            conn.close()
        except BaseException as e:
            errorMsg = f"MySql连接失败:{e}"
            results['state'] = False
            results['errorMsg'] = errorMsg
            cls_Logging.print_log(self,'error','connect_mysql',errorMsg)
        else:
            results['state'] = True
            results['dataBaseList'] = dataBaseList
        return results
