from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json

# Create your db here.
from FunManagement.models import FunManagement as db_FunManagement

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
                 "intNum": 0,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": i.uid.userName,
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
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'FunManagement', 'data_save', errorMsg)
    else:
        obj_db_FunManagement = db_FunManagement.objects.filter(
            is_del=0, sysType=sysType, pid_id=proId, page_id=pageId, funName=funName)
        if obj_db_FunManagement:
            response['errorMsg'] = "当前所属页面下已有相同的功能名称存在,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    db_FunManagement.objects.create(
                        sysType=sysType,
                        pid_id=proId,
                        page_id=pageId,
                        funName=funName,
                        remarks=remarks,
                        is_del=0,
                        uid_id=userId,
                        cuid=userId
                    )
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(proId),
                        cls_FindTable.get_page_name(pageId), funName,
                        userId,
                        None,
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
        if obj_db_FunManagement:
            select_db_FunManagement = db_FunManagement.objects.filter(
                sysType=sysType, pid_id=proId, page_id=pageId, funName=funName, is_del=0)
            if select_db_FunManagement:
                if funId == select_db_FunManagement[0].id:  # 自己修改自己
                    is_Edit = True
                else:
                    response['errorMsg'] = '当前页面下已有重复功能名称,请更改!'
            else:
                is_Edit = True
            if is_Edit:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        obj_db_FunManagement.update(
                            page_id=pageId,
                            funName=funName,
                            uid_id=userId,
                            remarks=remarks,
                            updateTime=cls_Common.get_date_time())
                        # region 添加操作信息
                        oldData = list(obj_db_FunManagement.values())
                        newData = dict(request.POST)
                        cls_Logging.record_operation_info(
                            'API', 'Manual', 3, 'Edit',
                            cls_FindTable.get_pro_name(proId),
                            cls_FindTable.get_page_name(pageId), funName,
                            userId,
                            None,
                            oldData,newData
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
        if obj_db_FunManagement:
            obj_db_FunManagement.update(
                is_del=1,
                updateTime=cls_Common.get_date_time(),
                uid_id=userId
            )
            # region 添加操作信息
            cls_Logging.record_operation_info(
                'API', 'Manual', 3, 'Delete',
                cls_FindTable.get_pro_name(obj_db_FunManagement[0].pid_id),
                cls_FindTable.get_page_name(obj_db_FunManagement[0].page_id),
                cls_FindTable.get_fun_name(funId),
                userId,
                None,
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
