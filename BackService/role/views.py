from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
# from django.db import transaction

import json

# Create your db here.
from role.models import BasicRole as db_BasicRole

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
        cls_Logging.record_error_info('Home', '2', 'role>select_data', errorMsg)
    else:
        obj_db_BasicRole = db_BasicRole.objects.filter(is_del=0).order_by('updateTime').order_by('dataType')
        select_db_BasicRole = obj_db_BasicRole[minSize: maxSize]
        if roleName:
            obj_db_BasicRole = obj_db_BasicRole.filter(roleName__icontains=roleName)
            select_db_BasicRole = obj_db_BasicRole[minSize: maxSize]
        for i in select_db_BasicRole:
            dataList.append(
                {"id": i.id,
                 "roleName": i.roleName,
                 "bindUsers": [],
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": i.uid.userName,
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_BasicRole.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleName = request.POST['roleName']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', '2', 'role>save_data', errorMsg)
    else:
        obj_db_BasicRole = db_BasicRole.objects.filter(is_del='0', roleName=roleName)
        if obj_db_BasicRole:
            response['errorMsg'] = '当前新增角色名称存在,请更改！'
        else:
            db_BasicRole.objects.create(
                roleName=roleName,
                dataType=1,
                uid_id=userId,
                is_del=0,
            )
            response['statusCode'] = 2001
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def edit_data(request):
    response = {}
    update_db_BasicRole = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = request.POST['roleId']
        roleName = request.POST['roleName']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', '2', 'role>save_data', errorMsg)
    else:
        obj_db_BasicRole = db_BasicRole.objects.filter(id=roleId)
        if obj_db_BasicRole[0].dataType == 0:  # 系统级别数据
            response['errorMsg'] = '系统级别角色不可修改!'
        else:
            obj_db_BasicRole = db_BasicRole.objects.filter(roleName=roleName, is_del='0')
            if obj_db_BasicRole:
                if roleId == obj_db_BasicRole[0].id:  # 自己修改自己
                    update_db_BasicRole = obj_db_BasicRole.filter(is_del='0', id=roleId).update(
                        roleName=roleName,
                        uid_id=userId,
                        updateTime=cls_Common.get_date_time())
                else:
                    response['errorMsg'] = '已有重复角色,请更改!'
            else:
                update_db_BasicRole = db_BasicRole.objects.filter(is_del='0', id=roleId).update(
                    roleName=roleName,
                    uid_id=userId,
                    updateTime=cls_Common.get_date_time())
        if update_db_BasicRole:
            response['statusCode'] = 2002
        return JsonResponse(response)
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = request.POST['roleId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', '2', 'role>delete_data', errorMsg)
    else:
        obj_db_BasicRole = db_BasicRole.objects.filter(is_del='0', id=roleId)
        if obj_db_BasicRole:
            obj_db_BasicRole.update(
                is_del=1,
                uid_id=userId,
                updateTime=cls_Common.get_date_time()
            )
            response['statusCode'] = 2003
        else:
            response['errorMsg'] = "该数据不存在于数据库中!"
    return JsonResponse(response)


@cls_Logging.log
@require_http_methods(["GET"])  # 无TOKEN的获取,只有主页用来获取角色，不可在系统内使用
def get_role_name_items(request):
    response = {}
    dataList = []
    obj_db_BasicRole = db_BasicRole.objects.filter(is_del=0).order_by('dataType')
    for i in obj_db_BasicRole:
        dataList.append({
            'label': i.roleName, 'value': i.id
        })
    response['itemsData'] = dataList
    response['statusCode'] = 2000
    return JsonResponse(response)
