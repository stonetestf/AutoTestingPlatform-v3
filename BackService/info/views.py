from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json

# Create your db here.
from info.models import OperateInfo as db_OperateInfo
from info.models import PushInfo as db_PushInfo
from login.models import UserTable as db_UserTable

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
@require_http_methods(["GET"])  # 操作信息
def select_operational_info(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        sysType = objData.sysType
        remindType = objData.remindType
        isRead = objData.isRead

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', 'info', 'select_operational_info', errorMsg)
    else:
        obj_db_OperateInfo = db_OperateInfo.objects.filter().order_by('-createTime')
        select_db_OperateInfo = obj_db_OperateInfo[minSize: maxSize]

        if sysType:
            obj_db_OperateInfo = obj_db_OperateInfo.filter(sysType=sysType)
            select_db_OperateInfo = obj_db_OperateInfo[minSize: maxSize]
        if remindType:
            obj_db_OperateInfo = obj_db_OperateInfo.filter(remindType=remindType)
            select_db_OperateInfo = obj_db_OperateInfo[minSize: maxSize]
        if isRead:
            obj_db_OperateInfo = obj_db_OperateInfo.filter(is_read=isRead)
            select_db_OperateInfo = obj_db_OperateInfo[minSize: maxSize]

        for i in select_db_OperateInfo:
            dataList.append({
                'id': i.id,
                'level': i.level,
                'remindType': i.remindType,
                'sysType': i.sysType,
                'toPage': i.toPage,
                'toFun': i.toFun,
                'info': i.info,
                # 'CUFront': i.CUFront,
                # 'CURear': i.CURear,
                'is_read': i.is_read,
                'userName': i.uid.userName,
                'createTime': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_OperateInfo.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 独立用户的操作信息
def user_operational_info(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', 'info', 'select_operational_info', errorMsg)
    else:
        obj_db_OperateInfo = db_OperateInfo.objects.filter(
            uid_id=userId, is_read=0, remindType__in=('Error', 'Warning')).order_by('-createTime')
        select_db_OperateInfo = obj_db_OperateInfo[minSize: maxSize]

        for i in select_db_OperateInfo:
            dataList.append({
                'id': i.id,
                'level': i.level,
                'remindType': i.remindType,
                'sysType': i.sysType,
                'toPage': i.toPage,
                'toFun': i.toFun,
                'info': i.info,
                # 'CUFront': i.CUFront,
                # 'CURear': i.CURear,
                'is_read': i.is_read,
                'userName': i.uid.userName,
                'createTime': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
            })

        # 加载推送信息
        obj_db_UserTable = db_UserTable.objects.filter(id=userId)
        if obj_db_UserTable:
            if obj_db_UserTable[0].userName == 'admin':
                obj_db_PushInfo = db_PushInfo.objects.filter(received=0)
            else:
                obj_db_PushInfo = db_PushInfo.objects.filter(uid_id=userId, received=0)
            for i in obj_db_PushInfo:
                if i.oinfo.uid_id != userId:  # 排除创建者看到自己推给别人的信息
                    dataList.append({
                        'id': i.oinfo.id,
                        'level': i.oinfo.level,
                        'remindType': i.oinfo.remindType,
                        'sysType': i.oinfo.sysType,
                        'toPage': i.oinfo.toPage,
                        'toFun': i.oinfo.toFun,
                        'info': i.oinfo.info,
                        # 'CUFront': i.CUFront,
                        # 'CURear': i.CURear,
                        'is_read': i.oinfo.is_read,
                        'userName': i.oinfo.uid.userName,
                        'createTime': str(i.oinfo.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                    })

        response['TableData'] = dataList
        response['Total'] = obj_db_OperateInfo.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 更改未读为已读取
def edit_isread_state(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        infoId = request.POST['infoId']
        types = request.POST['types']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', 'info', 'edit_isread_state', errorMsg)
    else:
        try:
            with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                if types == 'ALL':  # 全读
                    obj_db_PushInfo = db_PushInfo.objects.filter(received=0, uid_id=userId)
                    for i in obj_db_PushInfo:
                        db_OperateInfo.objects.filter(id=i.oinfo_id).update(
                            updateTime=cls_Common.get_date_time(), is_read=1)

                    obj_db_PushInfo .update(updateTime=cls_Common.get_date_time(), received=1)
                else:
                    db_PushInfo.objects.filter(oinfo_id=infoId).update(
                        updateTime=cls_Common.get_date_time(), received=1)
                    db_OperateInfo.objects.filter(id=infoId).update(updateTime=cls_Common.get_date_time(), is_read=1)
        except BaseException as e:  # 自动回滚，不需要任何操作
            response['errorMsg'] = f"已读操作失败:{e}"
        else:
            response['statusCode'] = 2002
    return JsonResponse(response)
