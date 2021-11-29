from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json

# Create your db here.

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()


# Create your views here.
@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def select_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        roleName = objData.roleName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', 'role','select_data', errorMsg)
    else:
        # obj_db_BasicRole = db_BasicRole.objects.filter(is_del=0).order_by('updateTime').order_by('dataType')
        # select_db_BasicRole = obj_db_BasicRole[minSize: maxSize]
        # if roleName:
        #     obj_db_BasicRole = obj_db_BasicRole.filter(roleName__icontains=roleName)
        #     select_db_BasicRole = obj_db_BasicRole[minSize: maxSize]
        # for i in select_db_BasicRole:
        #     # region 绑定用户
        #     bindUsers = ""
        #     obj_db_UserBindRole = db_UserBindRole.objects.filter(role_id=i.id,is_del=0)
        #     for index, item_BindRole in enumerate(obj_db_UserBindRole, 1):
        #         bindUsers += item_BindRole.user.userName
        #         if obj_db_UserBindRole.count() - index != 0:
        #             bindUsers += "、"
        #     # endregion
        #     dataList.append(
        #         {"id": i.id,
        #          "roleName": i.roleName,
        #          "bindUsers": bindUsers,
        #          "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
        #          "userName": i.uid.userName,
        #          }
        #     )

        response['TableData'] = dataList
        # response['Total'] = obj_db_BasicRole.count()
        response['statusCode'] = 2000
    return JsonResponse(response)