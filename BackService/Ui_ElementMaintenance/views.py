from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from Ui_ElementMaintenance.models import ElementBaseData as db_ElementBaseData
from Ui_ElementMaintenance.models import ElementLocation as db_ElementLocation
from Ui_ElementMaintenance.models import ElementHistory as db_ElementHistory

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

        proId = objData.proId
        pageId = objData.pageId
        funId = objData.funId
        elementName = objData.elementName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Ui_ElementMaintenance', 'select_data', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        if pageId:
            obj_db_ElementBaseData = obj_db_ElementBaseData.filter(page_id=pageId)
        if funId:
            obj_db_ElementBaseData = obj_db_ElementBaseData.filter(fun_id=funId)
        if elementName:
            obj_db_ElementBaseData = obj_db_ElementBaseData.filter(elementName__icontains=elementName)
        select_db_ElementBaseData = obj_db_ElementBaseData[minSize: maxSize]
        for i in select_db_ElementBaseData:
            tableItem = []
            obj_db_ElementLocation = db_ElementLocation.objects.filter(is_del=0, element_id=i.id).order_by('index')
            for item_location in obj_db_ElementLocation:
                tableItem.append({
                    'state': True if item_location.state == 1 else False,
                    'targetingType': item_location.targetingType,
                    'targetingPath': item_location.targetingPath,
                    'remarks': item_location.remarks,
                })
            dataList.append({
                "id": i.id,
                "elementName": i.elementName,
                "pageName": i.page.pageName,
                "funName": i.fun.funName,
                "elementType": i.elementType,
                "locationTotal": obj_db_ElementLocation.count(),
                "elementState":True if i.elementState==1 else False,
                "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
                "createUserName": cls_FindTable.get_userName(i.cuid),
                "tableItem": tableItem,
            })

        response['TableData'] = dataList
        response['Total'] = obj_db_ElementBaseData.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        proId = objData.baseData.proId
        pageId = objData.baseData.pageId
        funId = objData.baseData.funId
        elementName = objData.baseData.elementName
        elementType = objData.baseData.elementType
        elementState = 1 if objData.baseData.elementState else 0

        elementLocation = objData.elementLocation
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Ui_ElementMaintenance', 'save_data', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(
            is_del=0, pid_id=proId, fun_id=funId, page_id=pageId, elementName=elementName,elementType=elementType)
        if obj_db_ElementBaseData.exists():
            response['errorMsg'] = "当前所属功能下已有相同元素名称或元素类型,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'UI', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(proId),
                        cls_FindTable.get_page_name(pageId),
                        cls_FindTable.get_fun_name(funId),
                        userId,
                        '【新增元素】', CUFront=responseData
                    )
                    # endregion
                    # region 保存基本信息
                    save_db_ElementBaseData = db_ElementBaseData.objects.create(
                        pid_id=proId, page_id=pageId, fun_id=funId,
                        elementName=elementName, elementType=elementType,elementState=elementState,
                        uid_id=userId, cuid=userId, is_del=0, onlyCode=onlyCode,
                    )
                    # endregion
                    # region 定位表
                    product_list_to_insert = list()
                    for index, item_location in enumerate(elementLocation, 0):
                        product_list_to_insert.append(db_ElementLocation(
                            element_id=save_db_ElementBaseData.id,
                            index=index,
                            targetingType=item_location.targetingType,
                            targetingPath=item_location.targetingPath,
                            remarks=item_location.remarks,
                            state=1 if item_location.state else 0,
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ElementLocation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 添加历史恢复
                    restoreData = json.loads(json.dumps(request.POST))
                    restoreData['updateTime'] = save_db_ElementBaseData.updateTime.strftime('%Y-%m-%d %H:%M:%S')
                    restoreData['createTime'] = save_db_ElementBaseData.createTime.strftime('%Y-%m-%d %H:%M:%S')
                    restoreData['uid_id'] = save_db_ElementBaseData.uid_id
                    restoreData['cuid'] = save_db_ElementBaseData.cuid
                    restoreData['onlyCode'] = onlyCode
                    db_ElementHistory.objects.create(
                        pid_id=proId,
                        page_id=pageId,
                        fun_id=funId,
                        element_id=save_db_ElementBaseData.id,
                        elementName=elementName,
                        onlyCode=cls_Common.generate_only_code(),
                        operationType='Add',
                        restoreData=restoreData,
                        uid_id=userId,
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['elementId'] = save_db_ElementBaseData.id
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

        elementId = objData.elementId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Ui_ElementMaintenance', 'load_data', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(is_del=0, id=elementId)
        if obj_db_ElementBaseData.exists():
            baseData = {
                'pageId': obj_db_ElementBaseData[0].page_id,
                'funId': obj_db_ElementBaseData[0].fun_id,
                'elementName': obj_db_ElementBaseData[0].elementName,
                'elementType': ast.literal_eval(obj_db_ElementBaseData[0].elementType),
                'elementState':True if obj_db_ElementBaseData[0].elementState==1 else False,
            }
            obj_db_ElementLocation = db_ElementLocation.objects.filter(is_del=0, element_id=elementId).order_by('index')
            locationTable = [{'id': i.id,
                              'state': True if i.state == 1 else False,
                              'targetingType': i.targetingType,
                              'targetingPath': i.targetingPath,
                              'remarks': i.remarks
                              }
                             for i in obj_db_ElementLocation]

            response['statusCode'] = 2000
            response['baseData'] = baseData
            response['locationTable'] = locationTable
        else:
            response['errorMsg'] = "当前选择的数据不存在,请刷新列表后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def edit_data(request):
    response = {}
    is_Edit = False
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)

        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        elementId = int(objData.baseData.elementId)
        proId = objData.baseData.proId
        pageId = objData.baseData.pageId
        funId = objData.baseData.funId
        elementName = objData.baseData.elementName
        elementType = objData.baseData.elementType
        elementState = 1 if objData.baseData.elementState else 0
        elementLocation = objData.elementLocation
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Ui_ElementMaintenance', 'edit_data', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(id=elementId, is_del=0)
        if obj_db_ElementBaseData.exists():
            select_db_ElementBaseData = db_ElementBaseData.objects.filter(
                pid_id=proId,page_id=pageId,fun_id=funId,elementName=elementName, elementType=elementType,is_del=0)
            if select_db_ElementBaseData.exists():
                if elementId == select_db_ElementBaseData[0].id:  # 自己修改自己
                    is_Edit = True
                else:
                    response['errorMsg'] = '当前所属功能下已有重复元素名称或元素类型,请更改!'
            else:
                is_Edit = True
            if is_Edit:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 添加操作信息
                        oldData = list(obj_db_ElementBaseData.values())
                        newData = json.dumps(request.POST)
                        cls_Logging.record_operation_info(
                            "UI", 'Manual', 3, 'Edit',
                            cls_FindTable.get_pro_name(proId),
                            cls_FindTable.get_page_name(pageId),
                            cls_FindTable.get_fun_name(funId),
                            userId,
                            '【修改元素】',
                            oldData, newData
                        )
                        # endregion
                        # region 删除原数据
                        db_ElementLocation.objects.filter(
                            is_del=0, element_id=elementId, onlyCode=obj_db_ElementBaseData[0].onlyCode).update(
                            updateTime=cls_Common.get_date_time(), is_del=1
                        )
                        # endregion
                        # region 基本信息
                        obj_db_ElementBaseData.update(
                            pid_id=proId,
                            page_id=pageId,
                            fun_id=funId,
                            elementName=elementName,
                            elementType=elementType,
                            elementState=elementState,
                            updateTime=cls_Common.get_date_time(),
                            onlyCode=onlyCode,
                            uid_id=userId)
                        # endregion
                        # region 定位表
                        product_list_to_insert = list()
                        for index, item_location in enumerate(elementLocation, 0):
                            product_list_to_insert.append(db_ElementLocation(
                                element_id=elementId,
                                index=index,
                                targetingType=item_location.targetingType,
                                targetingPath=item_location.targetingPath,
                                remarks=item_location.remarks,
                                state=1 if item_location.state else 0,
                                is_del=0,
                                onlyCode=onlyCode)
                            )
                        db_ElementLocation.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 添加历史恢复
                        restoreData = json.loads(json.dumps(request.POST))
                        restoreData['updateTime'] = obj_db_ElementBaseData[0].updateTime.strftime('%Y-%m-%d %H:%M:%S')
                        restoreData['createTime'] = obj_db_ElementBaseData[0].createTime.strftime('%Y-%m-%d %H:%M:%S')
                        restoreData['uid_id'] = obj_db_ElementBaseData[0].uid_id
                        restoreData['cuid'] = obj_db_ElementBaseData[0].cuid
                        restoreData['onlyCode'] = onlyCode
                        db_ElementHistory.objects.create(
                            pid_id=proId,
                            page_id=pageId,
                            fun_id=funId,
                            element_id=elementId,
                            elementName=elementName,
                            onlyCode=cls_Common.generate_only_code(),
                            operationType='Edit',
                            restoreData=restoreData,
                            uid_id=userId,
                        )
                        # endregion
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'数据修改失败:{e}'
                else:
                    response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找当前所属页面,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        elementId = request.POST['elementId']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Ui_ElementMaintenance', 'delete_data', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(id=elementId)
        if obj_db_ElementBaseData.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加历史恢复
                    db_ElementHistory.objects.create(
                        pid_id=obj_db_ElementBaseData[0].pid_id,
                        page_id=obj_db_ElementBaseData[0].page_id,
                        fun_id=obj_db_ElementBaseData[0].fun_id,
                        element_id=elementId,
                        elementName=obj_db_ElementBaseData[0].elementName,
                        operationType='Delete',
                        onlyCode=onlyCode,
                        uid_id=userId,
                    )
                    # endregion
                    # region 删除关联信息
                    db_ElementLocation.objects.filter(
                        is_del=0,element_id=elementId,onlyCode=obj_db_ElementBaseData[0].onlyCode).update(
                        is_del=1, updateTime=cls_Common.get_date_time())
                    obj_db_ElementBaseData.update(
                        is_del=1, updateTime=cls_Common.get_date_time(),uid_id=userId
                    )
                    # endregion
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'UI', 'Manual', 3, 'Delete',
                        cls_FindTable.get_pro_name(obj_db_ElementBaseData[0].pid_id),
                        cls_FindTable.get_page_name(obj_db_ElementBaseData[0].page_id),
                        cls_FindTable.get_fun_name(obj_db_ElementBaseData[0].fun_id),
                        userId,
                        f'【删除元素】 ID:{elementId}:{obj_db_ElementBaseData[0].elementName}',
                        CUFront=json.dumps(request.POST)
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'数据删除失败:{e}'
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 效验接口数据的完成性
def charm_element_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        baseData = objData.baseData
        locationData = objData.locationData
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Ui_ElementMaintenance', 'charm_element_data', errorMsg)
    else:
        # region 验证 基本信息
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(
            is_del=0, pid_id=baseData.proId, fun_id=baseData.funId, page_id=baseData.pageId,
            elementName=baseData.elementName, elementType=baseData.elementType)
        if obj_db_ElementBaseData.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': "当前所属功能下已有相同元素名称或元素类型,请更改!",
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ElementBaseData.exists():
                    if baseData.elementId == obj_db_ElementBaseData[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': "当前所属功能下已有相同元素名称或元素类型,请更改!",
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 定位信息
        if locationData:
            stateList = []
            for index, item_location in enumerate(locationData, 1):
                stateList.append(item_location.state)
                if item_location.state:
                    if not item_location.targetingType:
                        dataList.append({
                            'stepsName': '定位信息',
                            'errorMsg': f'第{index}行:定位类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_location.targetingPath:
                        dataList.append({
                            'stepsName': '定位信息',
                            'errorMsg': f'第{index}行:定位地址不可为空!',
                            'updateTime': cls_Common.get_date_time()})
            if True not in stateList:
                dataList.append({
                    'stepsName': '定位信息',
                    'errorMsg': f'请至少保存或启用1条定位信息!',
                    'updateTime': cls_Common.get_date_time()})

        else:
            dataList.append({
                'stepsName': '定位信息',
                'errorMsg': f'请至少保存或启用1条定位信息!',
                'updateTime': cls_Common.get_date_time()})
        # endregion
        response['statusCode'] = 2000
        response['TableData'] = dataList
    return JsonResponse(response)



