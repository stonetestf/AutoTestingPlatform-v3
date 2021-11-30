# Create your db here.
from rest_framework.authtoken.models import Token as db_Token
from login.models import UserTable as db_UserTable
from login.models import UserBindRole as db_UserBindRole


# Create reference here.
from ClassData.Logger import Logging

# Create info here.
cls_Logging = Logging()


# Create your views here.
class FindTable(object):
    def get_userId(self,token):
        token = db_Token.objects.filter(key=token)  # 内置查询方法
        if token:
            obj_db_UserTable = db_UserTable.objects.filter(userId=token[0].user_id)
            if obj_db_UserTable:
                return obj_db_UserTable[0].id
            else:
                return None
        else:
            return None

    def get_roleId(self,userId):
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0,user_id=userId)
        if obj_db_UserBindRole:
            return obj_db_UserBindRole[0].role_id

        else:
            return None
