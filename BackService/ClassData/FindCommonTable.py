# Create your db here.
from rest_framework.authtoken.models import Token as db_Token
from login.models import UserTable as db_UserTable
from login.models import UserBindRole as db_UserBindRole
from ProjectManagement.models import ProManagement as db_ProManagement
from PageManagement.models import PageManagement as db_PageManagement
from FunManagement.models import FunManagement as db_FunManagement

# Create reference here.
from ClassData.Logger import Logging as cls_Logging

# Create info here.
# cls_Logging = Logging()


# Create your views here.
class FindTable(cls_Logging):
    def get_userId(self, token):  # 从Hearder中获取用户ID
        token = db_Token.objects.filter(key=token)  # 内置查询方法
        if token:
            obj_db_UserTable = db_UserTable.objects.filter(userId=token[0].user_id)
            if obj_db_UserTable:
                return obj_db_UserTable[0].id
            else:
                return None
        else:
            return None

    def get_roleId(self, userId):  # 返回角色ID
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0, user_id=userId)
        if obj_db_UserBindRole:
            return obj_db_UserBindRole[0].role_id

        else:
            return None

    def get_pro_name(self, proId):
        obj_db_ProManagement = db_ProManagement.objects.filter(id=proId)
        if obj_db_ProManagement:
            return obj_db_ProManagement[0].proName
        else:
            return None

    def get_page_name(self, pageId):
        obj_db_PageManagement = db_PageManagement.objects.filter(id=pageId)
        if obj_db_PageManagement:
            return obj_db_PageManagement[0].pageName
        else:
            return None

    def get_fun_name(self, funId):
        obj_db_FunManagement = db_FunManagement.objects.filter(id=funId)
        if obj_db_FunManagement:
            return obj_db_FunManagement[0].funName
        else:
            return None

