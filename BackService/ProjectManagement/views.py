from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json

# Create your db here.
from login.models import UserTable as db_UserTable
from role.models import BasicRole as db_BasicRole
from login.models import UserBindRole as db_UserBindRole
from ProjectManagement.models import ProManagement as db_ProManagement

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
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = objData.sysType
        proName = objData.proName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'select_data', errorMsg)
    else:
        obj_db_ProManagement = db_ProManagement.objects.filter(is_del=0, sysType=sysType).order_by('-updateTime')
        select_db_ProManagement = obj_db_ProManagement[minSize: maxSize]
        if proName:
            obj_db_ProManagement = obj_db_ProManagement.filter(proName__icontains=proName)
            select_db_ProManagement = obj_db_ProManagement[minSize: maxSize]
        for i in select_db_ProManagement:
            # region 查询创建人
            obj_db_UserTable = db_UserTable.objects.filter(is_del=0, id=i.cuid)
            if obj_db_UserTable:
                createUserName = obj_db_UserTable[0].userName
            else:
                createUserName = None
            # endregion
            # region 查询进入，修改，删除，的权限
            # 查询当前修改的用户是不是创建者
            if userId == i.cuid:
                isEdit = False
                isDelete = False
            else:
                # 查询当前查询的用户是不是管理员
                obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId)
                if obj_db_UserBindRole:
                    if obj_db_UserBindRole[0].role.dataType == 0:
                        isEdit = False
                        isDelete = False
                    else:
                        isEdit = True
                        isDelete = True
                else:
                    isEdit = True
                    isDelete = True
            # endregion
            dataList.append(
                {"id": i.id,
                 "proName": i.proName,
                 "remarks": i.remarks,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": i.uid.userName,
                 "createUserName": createUserName,
                 "isEdit":isEdit,
                 "isDelete":isDelete,
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_ProManagement.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = request.POST['sysType']
        proName = request.POST['proName']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'data_save', errorMsg)
    else:
        #  效验保存的数据
        obj_db_ProManagement = db_ProManagement.objects.filter(is_del=0, sysType=sysType, proName=proName)
        if obj_db_ProManagement:
            response['errorMsg'] = "已有相同的所属项目存在,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    db_ProManagement.objects.create(
                        sysType=sysType,
                        proName=proName,
                        remarks=remarks,
                        is_del=0,
                        uid_id=userId,
                        cuid=userId
                    )
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['statusCode'] = 2001
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def edit_data(request):
    response = {}
    is_edit = False
    update_db_ProManagement = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = request.POST['sysType']
        proId = int(request.POST['proId'])
        proName = request.POST['proName']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'edit_data', errorMsg)
    else:
        obj_db_ProManagement = db_ProManagement.objects.filter(id=proId)
        if obj_db_ProManagement:
            # 查询当前修改的用户是不是创建者
            if userId == obj_db_ProManagement[0].cuid:
                is_edit = True
            else:
                # 查询当前修改的用户是不是管理员成功
                obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId)
                if obj_db_UserBindRole:
                    if obj_db_UserBindRole[0].role.dataType == 0:
                        is_edit = True
                    else:
                        response['errorMsg'] = '您当前没有权限对此进行操作,只有创建者或超管组才有此操作权限!'
                else:
                    response['errorMsg'] = '当前用户未绑定角色组!'
            if is_edit:
                obj_db_ProManagement = db_ProManagement.objects.filter(proName=proName, is_del=0)
                if obj_db_ProManagement:
                    if proId == obj_db_ProManagement[0].id:  # 自己修改自己
                        update_db_ProManagement = db_ProManagement.objects.filter(is_del=0, id=proId).update(
                            sysType=sysType,
                            proName=proName,
                            uid_id=userId,
                            remarks=remarks,
                            updateTime=cls_Common.get_date_time())
                    else:
                        response['errorMsg'] = '已有重复角色,请更改!'
                else:
                    update_db_ProManagement = db_ProManagement.objects.filter(is_del=0, id=proId).update(
                        sysType=sysType,
                        proName=proName,
                        uid_id=userId,
                        remarks=remarks,
                        updateTime=cls_Common.get_date_time())
        else:
            response['errorMsg'] = '未找到当前项目,请刷新后重新尝试!'
    if update_db_ProManagement:
        response['statusCode'] = 2002
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    is_edit = False
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        proId = request.POST['proId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'delete_data', errorMsg)
    else:
        obj_db_ProManagement = db_ProManagement.objects.filter(id=proId)
        if obj_db_ProManagement:
            # 查询当前修改的用户是不是创建者
            if userId == obj_db_ProManagement[0].cuid:
                is_edit = True
            else:
                # 查询当前修改的用户是不是管理员成功
                obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId)
                if obj_db_UserBindRole:
                    if obj_db_UserBindRole[0].role.dataType == 0:
                        is_edit = True
                    else:
                        response['errorMsg'] = '您当前没有权限对此进行操作,只有创建者或超管组才有此操作权限!'
                else:
                    response['errorMsg'] = '当前用户未绑定角色组!'
            if is_edit:
                db_ProManagement.objects.filter(id=proId).update(
                    is_del=1,
                    updateTime=cls_Common.get_date_time()
                )
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前项目,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])# 加载角色下有哪些用户
def get_role_user_name_items(request):
    response = {}
    dataList = []

    obj_db_BasicRole = db_BasicRole.objects.filter(is_del=0).order_by('dataType')
    for i in obj_db_BasicRole:
        children = []
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0,role_id=i.id)
        for item in obj_db_UserBindRole:
            children.append({'label':item.user.userName,'value':item.user_id})
        dataList.append({
            'label': i.roleName, 'value': i.id,'children':children
        })
    response['itemsData'] = dataList
    response['statusCode'] = 2000
    return JsonResponse(response)