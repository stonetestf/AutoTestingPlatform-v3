from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json

# Create your db here.
from PageManagement.models import PageManagement as db_PageManagement

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
        pageName = objData.pageName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageMaintenancet', 'select_data', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(
            is_del=0, sysType=sysType, pid_id=proId).order_by('-updateTime')
        select_db_PageManagement = obj_db_PageManagement[minSize: maxSize]
        if pageName:
            obj_db_PageManagement = obj_db_PageManagement.filter(pageName__icontains=pageName)
            select_db_PageManagement = obj_db_PageManagement[minSize: maxSize]
        for i in select_db_PageManagement:
            dataList.append(
                {"id": i.id,
                 "pageName": i.pageName,
                 "remarks": i.remarks,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": i.uid.userName,
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_PageManagement.count()
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
        pageName = request.POST['pageName']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageManagement', 'data_save', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(
            is_del=0, sysType=sysType, pid_id=proId,pageName=pageName)
        if obj_db_PageManagement:
            response['errorMsg'] = "当前所属项目下已有相同的所属页面存在,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    db_PageManagement.objects.create(
                        sysType=sysType,
                        pid_id=proId,
                        pageName=pageName,
                        remarks=remarks,
                        is_del=0,
                        uid_id=userId,
                        cuid=userId
                    )
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(proId), None, None,
                        userId,
                        pageName
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
    update_db_PageManagement = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = request.POST['sysType']
        proId = request.POST['proId']
        pageId = int(request.POST['pageId'])
        pageName = request.POST['pageName']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageManagement', 'edit_data', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(id=pageId, is_del=0)
        if obj_db_PageManagement:
            select_db_PageManagement = db_PageManagement.objects.filter(
                sysType=sysType,pid_id=proId,pageName=pageName, is_del=0)
            if select_db_PageManagement:
                if pageId == select_db_PageManagement[0].id:  # 自己修改自己
                    update_db_PageManagement = db_PageManagement.objects.filter(is_del=0, id=pageId).update(
                        pageName=pageName,
                        uid_id=userId,
                        remarks=remarks,
                        updateTime=cls_Common.get_date_time())
                else:
                    response['errorMsg'] = '当前项目下已有重复页面名称,请更改!'
            else:
                update_db_PageManagement = db_PageManagement.objects.filter(is_del=0, id=pageId).update(
                    pageName=pageName,
                    uid_id=userId,
                    remarks=remarks,
                    updateTime=cls_Common.get_date_time())
        else:
            response['errorMsg'] = '未找当前所属页面,请刷新后重新尝试!'
    if update_db_PageManagement:
        response['statusCode'] = 2002
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        pageId = request.POST['pageId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageManagement', 'delete_data', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(id=pageId,is_del=0)
        if obj_db_PageManagement:
            obj_db_PageManagement.update(
                is_del=1,
                updateTime=cls_Common.get_date_time(),
                uid_id=userId,
            )
            response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前所属页面,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def get_page_name_items(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageMaintenancet', 'get_page_name_items', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(is_del=0,pid_id=proId).order_by('-updateTime')
        for i in obj_db_PageManagement:
            dataList.append({
                'label': i.pageName, 'value': i.id
            })
        response['itemsData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)
