from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from login.models import UserTable as db_UserTable
from login.models import UserBindRole as db_UserBindRole
from ProjectManagement.models import ProManagement as db_ProManagement
from ProjectManagement.models import ProBindMembers as db_ProBindMembers
from PageManagement.models import PageManagement as db_PageManagement
from ProjectManagement.models import ProHistory as db_ProHistory

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
            bindMembers = []
            # region 查询创建人
            obj_db_UserTable = db_UserTable.objects.filter(is_del=0, id=i.cuid)
            if obj_db_UserTable:
                createUserName = obj_db_UserTable[0].userName
            else:
                createUserName = None
            # endregion
            # region 查询进入，修改，删除，的权限
            if userId == i.cuid:
                isMembers = False
                isEdit = False
                isDelete = False
            else:
                # region 查询当前查询的用户是不是管理员
                obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId)
                if obj_db_UserBindRole:
                    if obj_db_UserBindRole[0].role.is_admin == 1:
                        isMembers = False
                        isEdit = False
                        isDelete = False
                    else:
                        isMembers = True
                        isEdit = True
                        isDelete = True
                else:
                    isMembers = True
                    isEdit = True
                    isDelete = True
                # endregion
            # region 查询当前用户是否有进入权限
            obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, pid_id=i.id, uid_id=userId)
            if obj_db_ProBindMembers:
                isEnterInto = False
            else:
                isEnterInto = True
                # endregion
            # endregion
            # region 查询当前项目关联的人员
            obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, pid_id=i.id)
            for item in obj_db_ProBindMembers:
                bindMembers.append({'id': item.uid.id, 'name': item.uid.nickName})  # 载入关联的成员
            # endregion
            # endregion
            dataList.append(
                {"id": i.id,
                 "proName": i.proName,
                 "remarks": i.remarks,
                 "bindMembers": bindMembers,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": i.uid.userName,
                 "createUserName": createUserName,
                 "isEnterInto": isEnterInto,
                 "isMembers": isMembers,
                 "isEdit": isEdit,
                 "isDelete": isDelete,
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
        roleId = cls_FindTable.get_roleId(userId)
        sysType = request.POST['sysType']
        proName = request.POST['proName']
        remarks = request.POST['remarks']
        getDateTime = cls_Common.get_date_time()
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
                        # restoreData = {
                        #     'sysType': sysType,
                        #     'proName': proName,
                        #     'remarks': remarks,
                        #     'is_del': 0,
                        #     'uid_id': userId,
                        #     'cuid': userId,
                        #     'createTime': getDateTime,
                        # }
                        db_ProHistory.objects.create(
                            pid_id=save_db_ProManagement.id,
                            proName=proName,
                            onlyCode=cls_Common.generate_only_code(),
                            operationType='Add',
                            restoreData=None,
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


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def edit_data(request):
    response = {}
    is_edit = False
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        is_admin = cls_FindTable.get_role_is_admin(roleId)
        sysType = request.POST['sysType']
        proId = int(request.POST['proId'])
        proName = request.POST['proName']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'edit_data', errorMsg)
    else:
        obj_db_ProManagement = db_ProManagement.objects.filter(id=proId, is_del=0)
        oldData = list(obj_db_ProManagement.values())
        newData = json.dumps(request.POST)
        if obj_db_ProManagement.exists():
            # 查询当前修改的用户是不是创建者
            if userId == obj_db_ProManagement[0].cuid:
                is_edit = True
            else:
                # 查询当前修改的用户是不是管理员成功
                obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId)
                if obj_db_UserBindRole.exists():
                    if is_admin:
                        is_edit = True
                    else:
                        response['errorMsg'] = '您当前没有权限对此进行操作,只有创建者或超管组才有此操作权限!'
                else:
                    response['errorMsg'] = '当前用户未绑定角色组!'
            if is_edit:
                select_db_ProManagement = db_ProManagement.objects.filter(sysType=sysType, proName=proName, is_del=0)
                if select_db_ProManagement.exists():
                    if proId == select_db_ProManagement[0].id:  # 自己修改自己
                        try:
                            with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                                db_ProManagement.objects.filter(is_del=0, id=proId).update(
                                    sysType=sysType,
                                    proName=proName,
                                    uid_id=userId,
                                    remarks=remarks,
                                    updateTime=cls_Common.get_date_time())
                                # region 添加操作信息
                                cls_Logging.record_operation_info(
                                    'API', 'Manual', 3, 'Edit',
                                    proName, None, None,
                                    userId,
                                    "修改项目",
                                    oldData, newData
                                )
                                # endregion
                                # region 添加历史恢复
                                oldData[0]['createTime'] = str(oldData[0]['createTime'].strftime('%Y-%m-%d %H:%M:%S'))
                                oldData[0]['updateTime'] = str(oldData[0]['updateTime'].strftime('%Y-%m-%d %H:%M:%S'))
                                db_ProHistory.objects.create(
                                    pid_id=proId,
                                    proName=proName,
                                    onlyCode=cls_Common.generate_only_code(),
                                    operationType='Edit',
                                    restoreData=oldData[0]
                                )
                                # endregion
                        except BaseException as e:  # 自动回滚，不需要任何操作
                            response['errorMsg'] = f'更新数据失败:{e}'
                        else:
                            response['statusCode'] = 2002
                    else:
                        response['errorMsg'] = '已有重复所属项目名称,请更改!'
                else:
                    try:
                        with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                            # region 添加操作信息
                            cls_Logging.record_operation_info(
                                'API', 'Manual', 3, 'Edit',
                                proName, None, None,
                                userId,
                                None,
                                oldData, newData
                            )
                            # endregion
                            db_ProManagement.objects.filter(is_del=0, id=proId).update(
                                sysType=sysType,
                                proName=proName,
                                uid_id=userId,
                                remarks=remarks,
                                updateTime=cls_Common.get_date_time())
                            # region 添加历史恢复
                            oldData[0]['createTime'] = str(oldData[0]['createTime'].strftime('%Y-%m-%d %H:%M:%S'))
                            oldData[0]['updateTime'] = str(oldData[0]['updateTime'].strftime('%Y-%m-%d %H:%M:%S'))
                            db_ProHistory.objects.create(
                                pid_id=proId,
                                proName=proName,
                                onlyCode=cls_Common.generate_only_code(),
                                operationType='Edit',
                                restoreData=oldData[0]
                            )
                            # endregion
                    except BaseException as e:  # 自动回滚，不需要任何操作
                        response['errorMsg'] = f'更新数据失败:{e}'
                    else:
                        response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找到当前项目,请刷新后重新尝试!'
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
        if obj_db_ProManagement.exists():
            obj_db_PageManagement = db_PageManagement.objects.filter(is_del=0, pid_id=proId)
            if obj_db_PageManagement.exists():
                response['errorMsg'] = '当前项目下有所属页面数据,请删除下级所属页面后在重新尝试删除!'
            else:
                # 查询当前修改的用户是不是创建者
                if userId == obj_db_ProManagement[0].cuid:
                    is_edit = True
                else:
                    # 查询当前修改的用户是不是管理员成功
                    obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId)
                    if obj_db_UserBindRole.exists():
                        if obj_db_UserBindRole[0].role.is_admin == 1:
                            is_edit = True
                        else:
                            response['errorMsg'] = '您当前没有权限对此进行操作,只有创建者或超管组才有此操作权限!'
                    else:
                        response['errorMsg'] = '当前用户未绑定角色组!'
                if is_edit:
                    try:
                        with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                            obj_db_ProManagement.update(
                                is_del=1, uid_id=userId, updateTime=cls_Common.get_date_time()
                            )
                            # 删除人员绑定表
                            db_ProBindMembers.objects.filter(pid_id=proId, is_del=0).update(
                                is_del=1, updateTime=cls_Common.get_date_time()
                            )
                            # region 添加操作信息
                            cls_Logging.record_operation_info(
                                'API', 'Manual', 3, 'Delete',
                                obj_db_ProManagement[0].proName, None, None,
                                userId,
                                '删除项目', CUFront=json.dumps(request.POST)
                            )
                            # endregion
                            # region 添加历史恢复
                            # oldData = list(obj_db_ProManagement.values())
                            # oldData[0]['createTime'] = str(oldData[0]['createTime'].strftime('%Y-%m-%d %H:%M:%S'))
                            # oldData[0]['updateTime'] = str(oldData[0]['updateTime'].strftime('%Y-%m-%d %H:%M:%S'))
                            # restoreData = {
                            #     'sysType': oldData[0]['sysType'],
                            #     'proName': oldData[0]['proName'],
                            #     'remarks': oldData[0]['remarks'],
                            #     'is_del': oldData[0]['is_del'],
                            #     'uid_id': oldData[0]['uid_id'],
                            #     'cuid': oldData[0]['cuid'],
                            #     'createTime': oldData[0]['createTime'],
                            #     'updateTime':oldData[0]['updateTime'],
                            # }
                            db_ProHistory.objects.create(
                                pid_id=proId,
                                proName=obj_db_ProManagement[0].proName,
                                onlyCode=cls_Common.generate_only_code(),
                                operationType='Delete',
                                restoreData=None,
                            )
                            # endregion
                    except BaseException as e:  # 自动回滚，不需要任何操作
                        response['errorMsg'] = f'删除失败:{e}'
                    else:
                        response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前项目,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 查询已加入项目的成员
def select_join_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        proId = objData.proId
        roleId = objData.roleId
        userName = objData.userName
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'select_join_data', errorMsg)
    else:
        obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, pid_id=proId)
        if roleId:
            obj_db_ProBindMembers = obj_db_ProBindMembers.filter(role_id=roleId)
        if userName:
            obj_db_ProBindMembers = obj_db_ProBindMembers.filter(uid__userName__icontains=userName)
        for i in obj_db_ProBindMembers:
            dataList.append({
                'id': i.uid.id,
                'roleName': i.role.roleName,
                'userName': i.uid.userName,
                'nickName': i.uid.nickName,
                'isLock': False if i.uid.is_lock == 0 else True,
            })

        response['TableData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 查询未加入项目的成员
def select_not_in_join_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        proId = objData.proId
        roleId = objData.roleId
        userName = objData.userName
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'select_not_in_join_data', errorMsg)
    else:
        obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, pid_id=proId)
        hasJoinedMembers = [i.uid.id for i in obj_db_ProBindMembers]

        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0)
        if roleId:
            obj_db_UserBindRole = obj_db_UserBindRole.filter(role_id=roleId)
        if userName:
            obj_db_UserBindRole = obj_db_UserBindRole.filter(user__userName__icontains=userName)
        for i in obj_db_UserBindRole:
            if i.user_id not in hasJoinedMembers:
                dataList.append({
                    'id': i.user.id,
                    'roleName': i.role.roleName,
                    'userName': i.user.userName,
                    'nickName': i.user.nickName,
                    'isLock': False if i.user.is_lock == 0 else True,
                })

        response['TableData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 加入成员
def join_members(request):
    response = {}
    try:
        proId = request.POST['proId']
        joinUserId = request.POST['userId']  # 需要加入项目的用户
        roleId = cls_FindTable.get_roleId(joinUserId)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'join_members', errorMsg)
    else:
        if roleId:
            db_ProBindMembers.objects.create(
                pid_id=proId,
                role_id=roleId,
                uid_id=joinUserId,
                is_del=0,
            )
            response['statusCode'] = 2002
        else:
            response['errorMsg'] = "当前选择的用户未加入到角色中,请联系管理员!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 删除成员
def delete_members(request):
    response = {}
    try:
        proId = request.POST['proId']
        userId = request.POST['userId']  # 需要加入项目的用户
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'delete_members', errorMsg)
    else:
        obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, pid_id=proId, uid_id=userId)
        if obj_db_ProBindMembers.exists():
            obj_db_ProBindMembers.update(
                updateTime=cls_Common.get_date_time(),
                is_del=1
            )
            response['statusCode'] = 2003
        else:
            response['errorMsg'] = "当前选择成员不存在于此项目中,请刷新后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 验证用户是否有进入此项目的权限
def verify_enter_into(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'verify_enter_into', errorMsg)
    else:
        obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, uid_id=userId, pid_id=proId)
        if obj_db_ProBindMembers.exists():
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = "当前用户不在此项目的成员列表中,不可进入!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 查询历史恢复
def select_history(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        sysType = objData.sysType
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'select_history', errorMsg)
    else:
        if proId:
            obj_db_ProHistory = db_ProHistory.objects.filter(pid_id=proId, pid__sysType=sysType).order_by('-createTime')
        else:
            obj_db_ProHistory = db_ProHistory.objects.filter(pid__sysType=sysType).order_by('-createTime')
        for i in obj_db_ProHistory:
            if i.restoreData:
                restoreData = json.dumps(ast.literal_eval(i.restoreData),
                                         sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)
            else:
                restoreData = None
            dataList.append({
                'id': i.id,
                'proName': i.proName,
                'operationType': i.operationType,
                'tableItem': [
                    {'restoreData': restoreData}
                ],
                'createTime': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                'userName': i.pid.uid.userName,
            })
        response['TableData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 恢复数据 只有管理员组或是项目创建人才可以恢复
def restor_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        is_admin = cls_FindTable.get_role_is_admin(roleId)
        historyId = request.POST['historyId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'restor_data', errorMsg)
    else:
        obj_db_ProHistory = db_ProHistory.objects.filter(id=historyId)
        if obj_db_ProHistory.exists():
            # 恢复时是管理员或是 当前项目的创建人时才可恢复
            if is_admin or obj_db_ProHistory[0].pid.cuid == userId:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        restoreData = obj_db_ProHistory[0].restoreData
                        if obj_db_ProHistory[0].operationType == "Edit":
                            restoreData = ast.literal_eval(restoreData)
                            db_ProManagement.objects.filter(id=obj_db_ProHistory[0].pid_id).update(
                                proName=restoreData['proName'],
                                remarks=restoreData['remarks'],
                                updateTime=cls_Common.get_date_time(),
                                createTime=restoreData['createTime'],
                                uid=userId,
                                is_del=0
                            )
                        else:  # Delete
                            obj_db_ProManagement = db_ProManagement.objects.filter(id=obj_db_ProHistory[0].pid_id)
                            if obj_db_ProManagement.exists():
                                obj_db_ProManagement.update(
                                    uid_id=userId, updateTime=cls_Common.get_date_time(), is_del=0
                                )
                            else:
                                response['errorMsg'] = "未找到当前可恢复的数据!"
                            # restoreData = ast.literal_eval(obj_db_ProHistory[0].restoreData)
                            # db_ProManagement.objects.create(
                            #     sysType=restoreData['sysType'],
                            #     proName=restoreData['proName'],
                            #     remarks=restoreData['remarks'],
                            #     updateTime=cls_Common.get_date_time(),
                            #     createTime=restoreData['createTime'],
                            #     uid_id=userId,
                            #     cuid=restoreData['cuid'],
                            #     is_del=0
                            # )
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f"数据恢复失败:{e}"
                else:
                    response['statusCode'] = 2002
            else:
                response['errorMsg'] = "您没有权限进行此操作,请联系项目的创建者或是管理员!"
        else:
            response['errorMsg'] = "当前选择的恢复数据不存在,请刷新后重新尝试!"
    return JsonResponse(response)