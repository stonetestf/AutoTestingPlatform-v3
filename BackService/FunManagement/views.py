from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from FunManagement.models import FunManagement as db_FunManagement
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData
from ProjectManagement.models import ProManagement as db_ProManagement
from PageManagement.models import PageManagement as db_PageManagement
from FunManagement.models import FunHistory as db_FunHistory

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
        sysType = objData.sysType
        proId = objData.proId
        pageId = objData.pageId
        funName = objData.funName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageMaintenancet', 'select_data', errorMsg)
    else:
        obj_db_FunManagement = db_FunManagement.objects.filter(
            is_del=0, sysType=sysType, pid_id=proId).order_by('-updateTime')
        select_db_FunManagement = obj_db_FunManagement[minSize: maxSize]
        if pageId:
            obj_db_FunManagement = obj_db_FunManagement.filter(page_id=pageId)
            select_db_FunManagement = obj_db_FunManagement[minSize: maxSize]
        if funName:
            obj_db_FunManagement = obj_db_FunManagement.filter(funName__icontains=funName)
            select_db_FunManagement = obj_db_FunManagement[minSize: maxSize]
        for i in select_db_FunManagement:
            dataList.append(
                {"id": i.id,
                 "pageId": i.page_id,
                 "pageName": i.page.pageName,
                 "funName": i.funName,
                 "remarks": i.remarks,
                 "apiNum": db_ApiBaseData.objects.filter(is_del=0,fun_id=i.id).count(),
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": f"{i.uid.userName}({i.uid.nickName})",
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_FunManagement.count()
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
        proId = request.POST['proId']
        pageId = request.POST['pageId']
        funName = request.POST['funName']
        remarks = request.POST['remarks']
        getDateTime = cls_Common.get_date_time()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'FunManagement', 'data_save', errorMsg)
    else:
        obj_db_FunManagement = db_FunManagement.objects.filter(
            is_del=0, sysType=sysType, pid_id=proId, page_id=pageId, funName=funName)
        if obj_db_FunManagement.exists():
            response['errorMsg'] = "当前所属页面下已有相同的功能名称存在,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 基本信息
                    save_db_FunManagement = db_FunManagement.objects.create(
                        sysType=sysType,
                        pid_id=proId,
                        page_id=pageId,
                        funName=funName,
                        remarks=remarks,
                        is_del=0,
                        uid_id=userId,
                        cuid=userId
                    )
                    # endregion
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(proId),
                        cls_FindTable.get_page_name(pageId), funName,
                        userId,
                        '新增功能',CUFront=json.dumps(request.POST)
                    )
                    # endregion
                    # region 添加历史恢复
                    # restoreData = {
                    #     'sysType': sysType,
                    #     'pid_id': proId,
                    #     'page_id': pageId,
                    #     'funName': funName,
                    #     'remarks': remarks,
                    #     'is_del': 0,
                    #     'uid_id': userId,
                    #     'cuid': userId,
                    #     'createTime': getDateTime,
                    # }
                    db_FunHistory.objects.create(
                        pid_id=proId,
                        page_id=pageId,
                        fun_id=save_db_FunManagement.id,
                        funName=funName,
                        onlyCode=cls_Common.generate_only_code(),
                        operationType='Add',
                        restoreData=None,
                    )
                    # endregion
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
    is_Edit = False
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = request.POST['sysType']
        funId = int(request.POST['funId'])
        proId = request.POST['proId']
        pageId = request.POST['pageId']
        funName = request.POST['funName']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'FunManagement', 'edit_data', errorMsg)
    else:
        obj_db_FunManagement = db_FunManagement.objects.filter(id=funId, is_del=0)
        if obj_db_FunManagement.exists():
            select_db_FunManagement = db_FunManagement.objects.filter(
                sysType=sysType, pid_id=proId, page_id=pageId, funName=funName, is_del=0)
            if select_db_FunManagement.exists():
                if funId == select_db_FunManagement[0].id:  # 自己修改自己
                    is_Edit = True
                else:
                    response['errorMsg'] = '当前页面下已有重复功能名称,请更改!'
            else:
                is_Edit = True
            if is_Edit:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 添加操作信息
                        oldData = list(obj_db_FunManagement.values())
                        newData = json.dumps(request.POST)
                        cls_Logging.record_operation_info(
                            'API', 'Manual', 3, 'Edit',
                            cls_FindTable.get_pro_name(proId),
                            cls_FindTable.get_page_name(pageId), funName,
                            userId,
                            '修改功能',
                            oldData, newData
                        )
                        # endregion
                        # region 基本信息
                        obj_db_FunManagement.update(
                            page_id=pageId,
                            funName=funName,
                            uid_id=userId,
                            remarks=remarks,
                            updateTime=cls_Common.get_date_time())
                        # endregion
                        # region 添加历史恢复
                        oldData[0]['createTime'] = str(oldData[0]['createTime'].strftime('%Y-%m-%d %H:%M:%S'))
                        oldData[0]['updateTime'] = str(oldData[0]['updateTime'].strftime('%Y-%m-%d %H:%M:%S'))
                        db_FunHistory.objects.create(
                            pid_id=proId,
                            page_id=pageId,
                            fun_id=funId,
                            funName=funName,
                            onlyCode=cls_Common.generate_only_code(),
                            operationType='Edit',
                            restoreData=oldData[0]
                        )
                        # endregion
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'数据修改失败:{e}'
                else:
                    response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找当前所属功能数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        funId = request.POST['funId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'FunManagement', 'delete_data', errorMsg)
    else:
        obj_db_FunManagement = db_FunManagement.objects.filter(id=funId)
        if obj_db_FunManagement.exists():
            obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0,fun_id=funId)
            if obj_db_ApiBaseData.exists():
                response['errorMsg'] = f'当前所属功能下存在 {obj_db_ApiBaseData.count()} 条接口信息,' \
                                       f'请删除或修改这些接口所属后在进行当前删除操作!'
            else:
                # region 基本信息
                obj_db_FunManagement.update(
                    is_del=1,
                    updateTime=cls_Common.get_date_time(),
                    uid_id=userId
                )
                # endregion
                # region 添加操作信息
                cls_Logging.record_operation_info(
                    'API', 'Manual', 3, 'Delete',
                    cls_FindTable.get_pro_name(obj_db_FunManagement[0].pid_id),
                    cls_FindTable.get_page_name(obj_db_FunManagement[0].page_id),
                    cls_FindTable.get_fun_name(funId),
                    userId,
                    '删除功能',CUFront=json.dumps(request.POST)
                )
                # endregion
                # region 添加历史恢复
                # oldData = list(obj_db_FunManagement.values())
                # oldData[0]['createTime'] = str(oldData[0]['createTime'].strftime('%Y-%m-%d %H:%M:%S'))
                # oldData[0]['updateTime'] = str(oldData[0]['updateTime'].strftime('%Y-%m-%d %H:%M:%S'))
                # restoreData = {
                #     'sysType': oldData[0]['sysType'],
                #     'pid_id': oldData[0]['pid_id'],
                #     'page_id': oldData[0]['page_id'],
                #     'funName': oldData[0]['funName'],
                #     'remarks': oldData[0]['remarks'],
                #     'is_del': oldData[0]['is_del'],
                #     'uid_id': oldData[0]['uid_id'],
                #     'cuid': oldData[0]['cuid'],
                #     'createTime': oldData[0]['createTime'],
                #     'updateTime': oldData[0]['updateTime'],
                # }
                db_FunHistory.objects.create(
                    pid_id=obj_db_FunManagement[0].pid_id,
                    page_id=obj_db_FunManagement[0].page_id,
                    fun_id=funId,
                    funName=obj_db_FunManagement[0].funName,
                    onlyCode=cls_Common.generate_only_code(),
                    operationType='Delete',
                    restoreData=None,
                )
                # endregion
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前功能数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def get_fun_name_items(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        proId = objData.proId
        pageId = objData.pageId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'FunManagement', 'get_fun_name_items', errorMsg)
    else:
        obj_db_FunManagement = db_FunManagement.objects.filter(
            is_del=0, pid_id=proId, page_id=pageId).order_by('-updateTime')
        for i in obj_db_FunManagement:
            dataList.append({
                'label': i.funName, 'value': i.id
            })
        response['itemsData'] = dataList
        response['statusCode'] = 2000
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
        funId = objData.funId
        funName = objData.funName
        operationType = objData.operationType

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'FunManagement', 'select_history', errorMsg)
    else:
        if funId:
            obj_db_FunHistory = db_FunHistory.objects.filter(
                fun_id=funId,page__sysType=sysType).order_by('-createTime')
        else:
            obj_db_FunHistory = db_FunHistory.objects.filter(page__sysType=sysType).order_by('-createTime')
            if funName:
                obj_db_FunHistory = obj_db_FunHistory.filter(funName__icontains=funName).order_by('-createTime')
            if operationType:
                obj_db_FunHistory = obj_db_FunHistory.filter(operationType=operationType).order_by('-createTime')
        select_db_FunHistory = obj_db_FunHistory[minSize: maxSize]
        for i in select_db_FunHistory:
            if i.restoreData:
                restoreData = json.dumps(ast.literal_eval(i.restoreData),
                                         sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)
            else:
                restoreData = None
            if restoreData:
                tableItem = [{'restoreData': restoreData}]
            else:
                tableItem = []
            dataList.append({
                'id': i.id,
                'funName': i.funName,
                'operationType': i.operationType,
                'tableItem': tableItem,
                'createTime': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                'userName': i.pid.uid.userName,
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_FunHistory.count()
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
        cls_Logging.record_error_info('API', 'FunManagement', 'restor_data', errorMsg)
    else:
        obj_db_FunHistory = db_FunHistory.objects.filter(id=historyId)
        if obj_db_FunHistory.exists():
            # 恢复时是管理员或是 当前项目的创建人时才可恢复
            if is_admin or obj_db_FunHistory[0].pid.cuid == userId:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        obj_db_ProManagement = db_ProManagement.objects.filter(is_del=0,id=obj_db_FunHistory[0].pid_id)
                        if obj_db_ProManagement.exists():
                            obj_db_PageManagement = db_PageManagement.objects.filter(
                                is_del=0,id=obj_db_FunHistory[0].page_id)
                            if obj_db_PageManagement.exists():
                                restoreData = obj_db_FunHistory[0].restoreData
                                if obj_db_FunHistory[0].operationType == "Edit":
                                    restoreData = ast.literal_eval(restoreData)
                                    db_FunManagement.objects.filter(id=obj_db_FunHistory[0].fun_id).update(
                                        pid_id=restoreData['pid_id'],
                                        page_id=restoreData['page_id'],
                                        funName=restoreData['funName'],
                                        remarks=restoreData['remarks'],
                                        updateTime=cls_Common.get_date_time(),
                                        createTime=restoreData['createTime'],
                                        uid=userId,
                                        is_del=0
                                    )
                                else:  # Delete
                                    obj_db_FunManagement = db_FunManagement.objects.filter(
                                        id=obj_db_FunHistory[0].fun_id)
                                    if obj_db_FunManagement.exists():
                                        obj_db_FunManagement.update(
                                            uid_id=userId, updateTime=cls_Common.get_date_time(), is_del=0
                                        )
                                    else:
                                        response['errorMsg'] = "未找到当前可恢复的数据!"
                            else:
                                response['errorMsg'] = f"当前恢复的数据上级所属页面不存在,恢复失败!"
                        else:
                            response['errorMsg'] = f"当前恢复的数据上级所属项目不存在,恢复失败!"
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f"数据恢复失败:{e}"
                else:
                    response['statusCode'] = 2002
            else:
                response['errorMsg'] = "您没有权限进行此操作,请联系项目的创建者或是管理员!"
        else:
            response['errorMsg'] = "当前选择的恢复数据不存在,请刷新后重新尝试!"
    return JsonResponse(response)
