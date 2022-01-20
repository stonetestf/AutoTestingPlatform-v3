from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.


# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.Redis import RedisHandle

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RedisHandle = RedisHandle()


# Create your views here.
@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        sysType = request.POST['sysType']
        proName = request.POST['proName']
        remarks = request.POST['remarks']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'data_save', errorMsg)
    else:
        if roleId:
            obj_db_ProManagement = db_ProManagement.objects.filter(is_del=0, sysType=sysType, proName=proName)
            if obj_db_ProManagement.exists():
                response['errorMsg'] = "已有相同的所属项目存在,请更改!"
            else:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 基本信息创建
                        save_db_ProManagement = db_ProManagement.objects.create(
                            sysType=sysType,
                            proName=proName,
                            remarks=remarks,
                            is_del=0,
                            uid_id=userId,
                            cuid=userId,
                            onlyCode=onlyCode,
                        )
                        # endregion
                        # region 绑定默认创建人到项目成员中
                        db_ProBindMembers.objects.create(
                            pid_id=save_db_ProManagement.id,
                            role_id=roleId,
                            uid_id=userId,
                            is_del=0
                        )
                        # endregion
                        # region 添加操作信息
                        cls_Logging.record_operation_info(
                            'API', 'Manual', 3, 'Add',
                            proName, None, None,
                            userId,
                            '新增项目', CUFront=json.dumps(request.POST)
                        )
                        # endregion
                        # region 添加历史恢复
                        restoreData = json.loads(json.dumps(request.POST))
                        restoreData['updateTime'] = save_db_ProManagement.updateTime.strftime('%Y-%m-%d %H:%M:%S')
                        restoreData['createTime'] = save_db_ProManagement.createTime.strftime('%Y-%m-%d %H:%M:%S')
                        restoreData['uid_id'] = save_db_ProManagement.uid_id
                        restoreData['cuid'] = save_db_ProManagement.cuid
                        restoreData['onlyCode'] = onlyCode

                        db_ProHistory.objects.create(
                            pid_id=save_db_ProManagement.id,
                            proName=proName,
                            onlyCode=onlyCode,
                            operationType='Add',
                            restoreData=restoreData,
                            uid_id=userId,
                        )
                        # endregion
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'保存失败:{e}'
                else:
                    response['statusCode'] = 2001
                    response['proId'] = save_db_ProManagement.id
                    response['proName'] = proName
        else:
            response['errorMsg'] = "当前用户无角色,请联系管理员"
    return JsonResponse(response)