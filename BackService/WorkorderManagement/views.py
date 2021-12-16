from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from login.models import UserTable as db_UserTable
from WorkorderManagement.models import WorkorderManagement as db_WorkorderManagement
from WorkorderManagement.models import WorkBindPushToUsers as db_WorkBindPushToUsers
from WorkorderManagement.models import WorkLifeCycle as db_WorkLifeCycle

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
        myWork = objData.myWork
        sysType = objData.sysType
        proId = objData.proId
        pageId = objData.pageId
        funId = objData.funId

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'WorkorderManagement', 'select_data', errorMsg)
    else:
        obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(
            is_del=0, sysType=sysType, pid_id=proId).order_by('-updateTime')
        select_db_WorkorderManagement = obj_db_WorkorderManagement[minSize: maxSize]
        if pageId:
            obj_db_WorkorderManagement = obj_db_WorkorderManagement.filter(page_id=pageId)
            select_db_WorkorderManagement = obj_db_WorkorderManagement[minSize: maxSize]
        if funId:
            obj_db_WorkorderManagement = obj_db_WorkorderManagement.filter(fun_id=funId)
            select_db_WorkorderManagement = obj_db_WorkorderManagement[minSize: maxSize]
        for i in select_db_WorkorderManagement:
            # region 查询创建人
            obj_db_UserTable = db_UserTable.objects.filter(is_del=0, id=i.cuid)
            if obj_db_UserTable:
                createUserName = obj_db_UserTable[0].userName
            else:
                createUserName = None
            # endregion
            if myWork == "My":
                obj_db_WorkBindPushToUsers = db_WorkBindPushToUsers.objects.filter(is_del=0, uid_id=userId)
                if obj_db_WorkBindPushToUsers or i.cuid == userId:
                    dataList.append(
                        {"id": i.id,
                         "workSource": i.workSource,
                         "workType": i.workType,
                         "pageName": i.page.pageName,
                         "funName": i.fun.funName,
                         "workName": i.workName,
                         "message": i.message,
                         "workState": i.workState,
                         "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                         "createUserName": createUserName,
                         })
            else:
                dataList.append(
                    {"id": i.id,
                     "workSource": i.workSource,
                     "workType": i.workType,
                     "pageName": i.page.pageName,
                     "funName": i.fun.funName,
                     "workName": i.workName,
                     "message": i.message,
                     "workState": i.workState,
                     "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                     "createUserName": createUserName,
                     })

        response['TableData'] = dataList
        response['Total'] = obj_db_WorkorderManagement.count()
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
        funId = request.POST['funId']
        workType = request.POST['workType']
        workState = request.POST['workState']
        workName = request.POST['workName']
        workMessage = request.POST['workMessage']
        pushTo = ast.literal_eval(request.POST['pushTo']) if request.POST['pushTo'] else []
        pushToList = [i for index, i in enumerate(pushTo, 1) if index % 2 == 0]
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'WorkorderManagement', 'data_save', errorMsg)
    else:
        # obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(
        #     is_del=0, sysType=sysType, pid_id=proId, page_id=pageId, fun_id=funId,workSource=0, workName=workName)
        # if obj_db_WorkorderManagement.exists():
        #     response['errorMsg'] = "当前所属功能下已有相同工单名称,请更改!"
        # else:
        try:
            with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                save_db_WorkorderManagement = db_WorkorderManagement.objects.create(
                    sysType=sysType,
                    pid_id=proId,
                    page_id=pageId,
                    fun_id=funId,
                    workSource=0,
                    workType=workType,
                    workState=workState,
                    workName=workName,
                    message=workMessage,
                    is_del=0,
                    uid_id=userId,
                    cuid=userId
                )
                # 添加操作信息
                operationInfoId = cls_Logging.record_operation_info(
                    'API', 'Manual', 3, "Add",
                    cls_FindTable.get_pro_name(proId),
                    cls_FindTable.get_page_name(pageId),
                    cls_FindTable.get_fun_name(funId),
                    userId,
                    f'编号:【A-{save_db_WorkorderManagement.id}】 {workName}:{workMessage}',
                    CUFront=json.dumps(request.POST)
                )
                # 添加工单的生命周期
                db_WorkLifeCycle.objects.create(
                    work_id=save_db_WorkorderManagement.id,
                    operationType='Add',
                    workState=workState,
                    uid_id=userId,
                    is_del=0,
                )
                if pushTo:  # 如果有推送To信息,就保存
                    product_list_to_insert = list()
                    for i in pushToList:
                        # 添加推送to数据
                        cls_Logging.push_to_user(operationInfoId, i)
                        product_list_to_insert.append(db_WorkBindPushToUsers(
                            work_id=save_db_WorkorderManagement.id,
                            uid_id=i,
                            is_del=0
                        ))
                    db_WorkBindPushToUsers.objects.bulk_create(product_list_to_insert)
        except BaseException as e:  # 自动回滚，不需要任何操作
            response['errorMsg'] = f'保存失败:{e}'
        else:
            response['statusCode'] = 2001
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        workId = objData.workId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'WorkorderManagement', 'load_edit_data', errorMsg)
    else:
        obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(is_del=0, id=workId)
        if obj_db_WorkorderManagement.exists():
            cuid = obj_db_WorkorderManagement[0].cuid
            data = obj_db_WorkorderManagement[0]
            pushTo = []
            obj_db_WorkBindPushToUsers = db_WorkBindPushToUsers.objects.filter(is_del=0, work_id=data.id)
            for i in obj_db_WorkBindPushToUsers:
                roleId = cls_FindTable.get_roleId(i.uid_id)
                pushTo.append([roleId, i.uid.id])

            # 在编辑时把创建人给加到推送TO中,省的反推时还要在添加
            roleId = cls_FindTable.get_roleId(cuid)
            if [roleId, cuid] not in pushTo:
                pushTo.append([roleId, cuid])
            dataTabel = {
                'workType': data.workType,
                'workState': data.workState,
                'pageId': data.page_id,
                'funId': data.fun_id,
                'workName': data.workName,
                'workMessage': data.message,
                'pushTo': pushTo,
            }

            response['statusCode'] = 2000
            response['dataTabel'] = dataTabel
        else:
            response['errorMsg'] = "当前选择的工单不存在,请刷新后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def edit_data(request):
    response = {}
    # is_edit = False
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        workId = int(request.POST['workId'])
        sysType = request.POST['sysType']
        proId = request.POST['proId']
        pageId = request.POST['pageId']
        funId = request.POST['funId']
        workType = request.POST['workType']
        workState = int(request.POST['workState'])
        workName = request.POST['workName']
        workMessage = request.POST['workMessage']
        pushTo = ast.literal_eval(request.POST['pushTo']) if request.POST['pushTo'] else []
        pushToList = [i for index, i in enumerate(pushTo, 1) if index % 2 == 0]
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'edit_data', errorMsg)
    else:
        obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(id=workId, is_del=0)
        if obj_db_WorkorderManagement.exists():
            # select_db_WorkorderManagement = db_WorkorderManagement.objects.filter(
            #     sysType=sysType, pid_id=proId, page_id=pageId, fun_id=funId, workName=workName, is_del=0)
            # if select_db_WorkorderManagement.exists():
            #     if workId == select_db_WorkorderManagement[0].id:  # 自己修改自己
            #         is_edit = True
            #     else:
            #         response['errorMsg'] = '已有重复工单,请更改!'
            # else:
            #     is_edit = True
            # if is_edit:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region添加操作信息
                    oldData = list(obj_db_WorkorderManagement.values())
                    newData = json.dumps(request.POST)
                    if workState != obj_db_WorkorderManagement[0].workState and workMessage == \
                            obj_db_WorkorderManagement[0].message:
                        # 0: 待受理, 1: 受理中, 2: 已解决, 3: 已关闭
                        if workState == 0:
                            workStateName = '待受理'
                        elif workState == 1:
                            workStateName = '受理中'
                        elif workState == 2:
                            workStateName = '已解决'
                        else:
                            workStateName = '已关闭'
                        message = f'工单编号:【A-{workId}】 修改状态:{workStateName}'
                    else:
                        message = f'工单编号:【A-{workId}】 {workName}:{workMessage}'
                    operationInfoId = cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Edit',
                        cls_FindTable.get_pro_name(proId),
                        cls_FindTable.get_page_name(pageId),
                        cls_FindTable.get_fun_name(funId),
                        userId,
                        # f'A-{workId}:{workName}',
                        message,
                        oldData, newData
                    )
                    # endregion
                    # region 基本信息
                    obj_db_WorkorderManagement.update(
                        sysType=sysType,
                        pid_id=proId,
                        page_id=pageId,
                        fun_id=funId,
                        workType=workType,
                        workState=workState,
                        workName=workName,
                        message=workMessage,
                        uid_id=userId,
                        updateTime=cls_Common.get_date_time()
                    )
                    # endregion
                    # region 添加工单的生命周期
                    db_WorkLifeCycle.objects.create(
                        work_id=workId,
                        operationType='Edit',
                        workState=workState,
                        operationInfo=newData,
                        uid_id=userId,
                        is_del=0,
                    )
                    # endregion
                    # # 在修改时如果正在修改的人是创建人才会重新推送信息
                    # if userId == obj_db_WorkorderManagement[0].cuid:
                    if pushTo:  # 如果有推送To信息,就保存
                        db_WorkBindPushToUsers.objects.filter(is_del=0, work_id=workId).update(
                            is_del=1, updateTime=cls_Common.get_date_time())
                        product_list_to_insert = list()
                        for i in pushToList:
                            # 添加推送to数据
                            cls_Logging.push_to_user(operationInfoId, i)
                            product_list_to_insert.append(db_WorkBindPushToUsers(
                                work_id=workId,
                                uid_id=i,
                                is_del=0
                            ))
                        db_WorkBindPushToUsers.objects.bulk_create(product_list_to_insert)
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'工单修改失败:{e}'
            else:
                response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找到当前工单,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        workId = request.POST['workId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'WorkorderManagement', 'delete_data', errorMsg)
    else:
        obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(id=workId)
        if obj_db_WorkorderManagement.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    obj_db_WorkorderManagement.update(is_del=1, uid_id=userId, updateTime=cls_Common.get_date_time())
                    db_WorkBindPushToUsers.objects.filter(is_del=0, work_id=workId).update(
                        is_del=1, updateTime=cls_Common.get_date_time()
                    )
                    db_WorkLifeCycle.objects.filter(is_del=0, work_id=workId).update(
                        is_del=1, updateTime=cls_Common.get_date_time()
                    )
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Delete',
                        cls_FindTable.get_pro_name(obj_db_WorkorderManagement[0].pid_id),
                        cls_FindTable.get_page_name(obj_db_WorkorderManagement[0].page_id),
                        cls_FindTable.get_fun_name(obj_db_WorkorderManagement[0].fun_id),
                        userId,
                        obj_db_WorkorderManagement[0].workName, CUFront=json.dumps(request.POST)
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f"当前工单删除失败:{e}"
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前工单信息,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def select_life_cycle(request):  # 获取当前工单的生命周期
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        workId = objData.workId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'WorkorderManagement', 'select_life_cycle', errorMsg)
    else:
        obj_db_WorkLifeCycle = db_WorkLifeCycle.objects.filter(work_id=workId).order_by('-updateTime')
        for i in obj_db_WorkLifeCycle:
            title = None
            content = None
            operationType = i.operationType
            if i.workState == 0:
                workState = '待受理'
            elif i.workState == 1:
                workState = '受理中'
            elif i.workState == 2:
                workState = '已解决'
            else:
                workState = '已关闭'
            if operationType == "Add":
                title = f'创建工单【{workState}】 {i.uid.userName}({i.uid.nickName})'
            elif operationType == "Edit":
                title = f'修改工单【{workState}】 {i.uid.userName}({i.uid.nickName})'
                content = json.dumps(
                    ast.literal_eval(i.operationInfo),
                    sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)
            dataList.append({
                'title': title,
                'content': content,
                'timestamp': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
            })
        response['statusCode'] = 2000
        response['dataTabel'] = dataList
    return JsonResponse(response)
