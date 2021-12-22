from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from ProjectManagement.models import ProManagement as db_ProManagement
from PageManagement.models import PageManagement as db_PageManagement
from FunManagement.models import FunManagement as db_FunManagement
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData
from Api_IntMaintenance.models import ApiHeaders as db_ApiHeaders
from Api_IntMaintenance.models import ApiParams as db_ApiParams
from Api_IntMaintenance.models import ApiBody as db_ApiBody
from Api_IntMaintenance.models import ApiExtract as db_ApiExtract
from Api_IntMaintenance.models import ApiValidate as db_ApiValidate
from Api_IntMaintenance.models import ApiOperation as db_ApiOperation
from Api_IntMaintenance.models import ApiAssociatedUser as db_ApiAssociatedUser
from Api_IntMaintenance.models import ApiDynamic as db_ApiDynamic
from WorkorderManagement.models import WorkorderManagement as db_WorkorderManagement
from WorkorderManagement.models import WorkBindPushToUsers as db_WorkBindPushToUsers
from WorkorderManagement.models import WorkLifeCycle as db_WorkLifeCycle
from Api_IntMaintenance.models import ApiHistory as db_ApiHistory
from PageEnvironment.models import PageEnvironment as db_PageEnvironment

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.Request import RequstOperation
from ClassData.TestReport import ApiReport

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RequstOperation = RequstOperation()
cls_ApiReport = ApiReport()


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
        proId = objData.proId
        pageId = objData.pageId
        funId = objData.funId
        apiName = objData.apiName
        requestUrl = objData.requestUrl
        apiState = objData.apiState
        associations = objData.associations
        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'select_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]
        if pageId:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(page_id=pageId)
            select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]
        if funId:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(fun_id=funId)
            select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]
        if apiName:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(apiName__icontains=apiName)
            select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]
        if requestUrl:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(requestUrl__icontains=requestUrl)
            select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]
        if apiState:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(apiState=apiState)
            select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]

        for i in select_db_ApiBaseData:
            obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(is_del=0, apiId_id=i.id, uid_id=userId)
            if obj_db_ApiAssociatedUser or userId == i.cuid:
                associationMy = True
            else:
                associationMy = False
            url = ast.literal_eval(i.requestUrl)
            callIndex = f'url{i.requestUrlRadio}'
            if associations == 'My':
                if associationMy:
                    dataList.append({
                        'id': i.id,
                        'pageId': i.page_id,
                        'pageName': i.page.pageName,
                        'funId': i.fun_id,
                        'funName': i.fun.funName,
                        'apiName': i.apiName,
                        'requestType': i.requestType,
                        'requestUrl': url[f'{callIndex}'],
                        'apiState': i.apiState,
                        'associationMy': associationMy,
                        'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                        'userName': i.uid.userName,
                        'createUserId': [[cls_FindTable.get_roleId(i.cuid), i.cuid]]
                    })
            else:
                dataList.append({
                    'id': i.id,
                    'pageId': i.page_id,
                    'pageName': i.page.pageName,
                    'funId': i.fun_id,
                    'funName': i.fun.funName,
                    'apiName': i.apiName,
                    'requestType': i.requestType,
                    'requestUrl': url[f'{callIndex}'],
                    'apiState': i.apiState,
                    'associationMy': associationMy,
                    'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                    'userName': i.uid.userName,
                    'createUserId': [[cls_FindTable.get_roleId(i.cuid), i.cuid]]
                })
        response['TableData'] = dataList
        response['Total'] = obj_db_ApiBaseData.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 效验接口数据的完成性
def charm_api_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        basicInfo = objData.BasicInfo
        apiInfo = objData.ApiInfo
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'charm_api_data', errorMsg)
    else:
        # region 验证 接口名称,请求类型,请求地址
        requestUrlRadio = apiInfo.requestUrlRadio
        requestUrl = responseData['ApiInfo']['requestUrl'][f'url{requestUrlRadio}']
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
            is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
            apiName=basicInfo.apiName, requestType=apiInfo.requestType, requestUrl=requestUrl)
        if obj_db_ApiBaseData.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属功能下已有相同接口名称,类型,请求地址,请更改!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ApiBaseData.exists():
                    if basicInfo.apiId == obj_db_ApiBaseData[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属功能下已有相同接口名称,类型,请求地址,请更改!',
                            'updateTime': cls_Common.get_date_time()})
        else:
            obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
                is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                apiName=basicInfo.apiName, requestType=apiInfo.requestType)
            if obj_db_ApiBaseData.exists():
                if charmType:
                    dataList.append({
                        'stepsName': '基本信息',
                        'errorMsg': '当前所属功能下已有相同接口名称,类型,请更改!',
                        'updateTime': cls_Common.get_date_time()})
                else:
                    if obj_db_ApiBaseData.exists():
                        if basicInfo.apiId == obj_db_ApiBaseData[0].id:
                            pass
                        else:
                            dataList.append({
                                'stepsName': '基本信息',
                                'errorMsg': '当前所属功能下已有相同接口名称,类型,请更改!',
                                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证请求URl

        if not requestUrl:
            dataList.append({
                'stepsName': '接口信息',
                'errorMsg': f"当前{f'url{requestUrlRadio}'},接口请求地址为空!",
                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 headers
        if apiInfo.request.headers:
            for index, item_headers in enumerate(apiInfo.request.headers, 1):
                if item_headers.state:
                    if not item_headers.key:
                        dataList.append({
                            'stepsName': '接口信息-Headers',
                            'errorMsg': f'第{index}行:参数名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 params
        if apiInfo.request.params:
            for index, item_params in enumerate(apiInfo.request.params, 1):
                if item_params.state:
                    if not item_params.key:
                        dataList.append({
                            'stepsName': '接口信息-Params',
                            'errorMsg': f'第{index}行:参数名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 body
        if apiInfo.request.body.requestSaveType == 'form-data':
            for index, item_body in enumerate(apiInfo.request.body.formData, 1):
                if item_body.state:
                    if not item_body.key:
                        dataList.append({
                            'stepsName': '接口信息-Body',
                            'errorMsg': f'第{index}行:参数名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 提取
        if apiInfo.request.extract:
            for index, item_extract in enumerate(apiInfo.request.extract, 1):
                if item_extract.state:
                    if not item_extract.key:
                        dataList.append({
                            'stepsName': '接口信息-Extract',
                            'errorMsg': f'第{index}行:变量名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_extract.value:
                        dataList.append({
                            'stepsName': '接口信息-Extract',
                            'errorMsg': f'第{index}行:提取表达式不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 断言
        if apiInfo.request.validate:
            for index, item_validate in enumerate(apiInfo.request.validate, 1):
                if item_validate.state:
                    if not item_validate.checkName:
                        dataList.append({
                            'stepsName': '接口信息-Validate',
                            'errorMsg': f'第{index}行:提取变量名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_validate.validateType:
                        dataList.append({
                            'stepsName': '接口信息-Validate',
                            'errorMsg': f'第{index}行:断言类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_validate.valueType:
                        dataList.append({
                            'stepsName': '接口信息-Validate',
                            'errorMsg': f'第{index}行:断言值类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 前置操作
        if apiInfo.request.preOperation:
            for index, item_preOperation in enumerate(apiInfo.request.preOperation, 1):
                if item_preOperation.state:
                    if item_preOperation.operationType == 'Methods':
                        if not item_preOperation.methodsName:
                            dataList.append({
                                'stepsName': '接口信息-前置操作',
                                'errorMsg': f'第{index}行:函数方法名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                        if '(' not in item_preOperation.methodsName or ')' not in item_preOperation.methodsName:
                            dataList.append({
                                'stepsName': '接口信息-前置操作',
                                'errorMsg': f'第{index}行:函数方法名称未检测到 ()',
                                'updateTime': cls_Common.get_date_time()})

                    elif item_preOperation.operationType == 'DataBase':
                        if not item_preOperation.dataBase:
                            dataList.append({
                                'stepsName': '接口信息-前置操作',
                                'errorMsg': f'第{index}行:当前没有选择需要执行的数据库!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_preOperation.sql:
                            dataList.append({
                                'stepsName': '接口信息-前置操作',
                                'errorMsg': f'第{index}行:请输入SQL语句!',
                                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 后置操作
        if apiInfo.request.rearOperation:
            for index, item_rearOperation in enumerate(apiInfo.request.rearOperation, 1):
                if item_rearOperation.state:
                    if item_rearOperation.operationType == 'Methods':
                        if not item_rearOperation.methodsName:
                            dataList.append({
                                'stepsName': '接口信息-后置操作',
                                'errorMsg': f'第{index}行:函数方法名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                        if '(' not in item_rearOperation.methodsName or ')' not in item_rearOperation.methodsName:
                            dataList.append({
                                'stepsName': '接口信息-后置操作',
                                'errorMsg': f'第{index}行:函数方法名称未检测到 ()',
                                'updateTime': cls_Common.get_date_time()})
                    elif item_rearOperation.operationType == 'DataBase':
                        if not item_rearOperation.dataBase:
                            dataList.append({
                                'stepsName': '接口信息-后置操作',
                                'errorMsg': f'第{index}行:当前没有选择需要执行的数据库!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_rearOperation.sql:
                            dataList.append({
                                'stepsName': '接口信息-后置操作',
                                'errorMsg': f'第{index}行:请输入SQL语句!',
                                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证params 和body 至少有1个有参数
        if not apiInfo.request.params and \
                not apiInfo.request.body.formData and \
                not apiInfo.request.body.raw and not apiInfo.request.body.requestSaveType == 'none':
            dataList.append({
                'stepsName': '接口信息-参数请求',
                'errorMsg': f'不可创建空参数请求,Params或Body请求中至少有1个不可为空!',
                'updateTime': cls_Common.get_date_time()})
        # endregion
        response['statusCode'] = 2000
        response['TableData'] = dataList
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])  # 当前操作者
        basicInfo = objData.BasicInfo
        apiInfo = objData.ApiInfo
        if basicInfo.assignedUserId:
            assignedUserId = basicInfo.assignedUserId[1]
        else:
            assignedUserId = userId
        requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
            apiInfo.request.params, apiInfo.request.body.formData, apiInfo.request.body.raw)
        historyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'data_save', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
            is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
            apiName=basicInfo.apiName, requestType=apiInfo.requestType,
            requestUrl=apiInfo.requestUrl._object_maker__data)
        if obj_db_ApiBaseData.exists():
            response['errorMsg'] = f'当前所属功能下已有相同数据,请修改后在继续保存!'
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    operationInfoId = cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        cls_FindTable.get_page_name(basicInfo.pageId),
                        cls_FindTable.get_fun_name(basicInfo.funId),
                        userId,
                        '【新增接口】', CUFront=responseData
                    )
                    # endregion
                    # region 保存基本信息
                    save_db_ApiBaseData = db_ApiBaseData.objects.create(
                        pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        apiName=basicInfo.apiName, environment_id=basicInfo.environmentId, apiState=basicInfo.apiState,
                        requestType=apiInfo.requestType, requestUrl=apiInfo.requestUrl._object_maker__data,
                        requestUrlRadio=apiInfo.requestUrlRadio,
                        requestParamsType='Body' if apiInfo.request.body.requestSaveType == 'none' else requestParamsType,
                        bodyRequestSaveType=apiInfo.request.body.requestSaveType,
                        uid_id=assignedUserId, cuid=userId, is_del=0,
                    )
                    product_list_to_insert = list()
                    for item_userId in basicInfo.pushTo:
                        product_list_to_insert.append(db_ApiAssociatedUser(
                            apiId_id=save_db_ApiBaseData.id,
                            opertateInfo_id=operationInfoId,
                            uid_id=item_userId[1],
                            is_del=0)
                        )
                    db_ApiAssociatedUser.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 添加历史恢复
                    db_ApiHistory.objects.create(
                        pid_id=basicInfo.proId,
                        page_id=basicInfo.pageId,
                        fun_id=basicInfo.funId,
                        api_id=save_db_ApiBaseData.id,
                        apiName=basicInfo.apiName,
                        operationType='Add',
                        restoreData=None,
                        onlyCode=historyCode,
                    )
                    # endregion
                    # region Headers
                    product_list_to_insert = list()
                    for item_headers in apiInfo.request.headers:
                        product_list_to_insert.append(db_ApiHeaders(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_headers.index,
                            key=item_headers.key,
                            value=item_headers.value,
                            remarks=item_headers.remarks,
                            state=1 if item_headers.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiHeaders.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Params
                    product_list_to_insert = list()
                    for item_params in apiInfo.request.params:
                        product_list_to_insert.append(db_ApiParams(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_params.index,
                            key=item_params.key,
                            value=item_params.value,
                            remarks=item_params.remarks,
                            state=1 if item_params.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiParams.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Body
                    if apiInfo.request.body.requestSaveType == 'form-data':
                        product_list_to_insert = list()
                        for item_body in apiInfo.request.body.formData:
                            product_list_to_insert.append(db_ApiBody(
                                apiId_id=save_db_ApiBaseData.id,
                                index=item_body.index,
                                key=item_body.key,
                                value=item_body.value,
                                remarks=item_body.remarks,
                                state=1 if item_body.state else 0,
                                is_del=0,
                                historyCode=historyCode)
                            )
                        db_ApiBody.objects.bulk_create(product_list_to_insert)
                    elif apiInfo.request.body.requestSaveType == 'raw':
                        db_ApiBody.objects.create(
                            apiId_id=save_db_ApiBaseData.id,
                            index=0,
                            key=None,
                            value=apiInfo.request.body.raw,
                            state=1,
                            is_del=0,
                            historyCode=historyCode
                        )
                    # file 之后在做
                    # endregion
                    # region Extract
                    product_list_to_insert = list()
                    for item_extract in apiInfo.request.extract:
                        product_list_to_insert.append(db_ApiExtract(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_extract.index,
                            key=item_extract.key,
                            value=item_extract.value,
                            remarks=item_extract.remarks,
                            state=1 if item_extract.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiExtract.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Validate
                    product_list_to_insert = list()
                    for item_validate in apiInfo.request.validate:
                        product_list_to_insert.append(db_ApiValidate(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_validate.index,
                            checkName=item_validate.checkName,
                            validateType=item_validate.validateType,
                            valueType=item_validate.valueType,
                            expectedResults=item_validate.expectedResults,
                            remarks=item_validate.remarks,
                            state=1 if item_validate.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiValidate.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 前置
                    product_list_to_insert = list()
                    for item_preOperation in apiInfo.request.preOperation:
                        product_list_to_insert.append(db_ApiOperation(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_preOperation.index,
                            location='Pre',
                            operationType=item_preOperation.operationType,
                            methodsName=item_preOperation.methodsName,
                            dataBaseId=item_preOperation.dataBase,
                            sql=item_preOperation.sql,
                            remarks=item_preOperation.remarks,
                            state=1 if item_preOperation.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 后置
                    product_list_to_insert = list()
                    for item_rearOperation in apiInfo.request.rearOperation:
                        product_list_to_insert.append(db_ApiOperation(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_rearOperation.index,
                            location='Rear',
                            operationType=item_rearOperation.operationType,
                            methodsName=item_rearOperation.methodsName,
                            dataBaseId=item_rearOperation.dataBase,
                            sql=item_rearOperation.sql,
                            remarks=item_rearOperation.remarks,
                            state=1 if item_rearOperation.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 创建被关联用户的新增提醒
                    obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(
                        is_del=0, apiId_id=save_db_ApiBaseData.id, historyCode=historyCode)
                    for item_associatedUser in obj_db_ApiAssociatedUser:
                        cls_Logging.push_to_user(operationInfoId, item_associatedUser.uid_id)
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
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        basicInfo = objData.BasicInfo
        apiInfo = objData.ApiInfo
        requestUrlRadio = apiInfo.requestUrlRadio
        if basicInfo.assignedUserId:
            assignedUserId = basicInfo.assignedUserId[1]
        else:
            assignedUserId = userId
        requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
            apiInfo.request.params, apiInfo.request.body.formData, apiInfo.request.body.raw)
        historyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'edit_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=basicInfo.apiId, is_del=0)
        if obj_db_ApiBaseData.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    # region 查询以前的数据
                    headers = []
                    params = []
                    body = []
                    extract = []
                    validate = []
                    preOperation = []
                    rearOperation = []
                    # region 基本信息
                    # region headers
                    obj_db_ApiHeaders = db_ApiHeaders.objects.filter(is_del=0, apiId_id=basicInfo.apiId).order_by(
                        'index')
                    for item_headers in obj_db_ApiHeaders:
                        headers.append({
                            'index': item_headers.index,
                            'key': item_headers.key,
                            'value': item_headers.value,
                            'remarks': item_headers.remarks,
                            'state': True if item_headers.state else False,
                        })
                    # endregion
                    # region params
                    obj_db_ApiParams = db_ApiParams.objects.filter(is_del=0, apiId_id=basicInfo.apiId).order_by('index')
                    for item_params in obj_db_ApiParams:
                        params.append({
                            'index': item_params.index,
                            'key': item_params.key,
                            'value': item_params.value,
                            'remarks': item_params.remarks,
                            'state': True if item_params.state else False,
                        })
                    # endregion
                    # region body
                    bodyData = None
                    obj_db_ApiBody = db_ApiBody.objects.filter(is_del=0, apiId_id=basicInfo.apiId).order_by('index')
                    if obj_db_ApiBaseData[0].bodyRequestSaveType == 'form-data':
                        for item_body in obj_db_ApiBody:
                            body.append({
                                'index': item_body.index,
                                'key': item_body.key,
                                'value': item_body.value,
                                'remarks': item_body.remarks,
                                'state': True if item_body.state else False,
                            })
                        bodyData = body
                    elif obj_db_ApiBaseData[0].bodyRequestSaveType == 'raw':
                        bodyData = obj_db_ApiBody[0].value
                    # endregion
                    # region extract
                    obj_db_ApiExtract = db_ApiExtract.objects.filter(is_del=0, apiId_id=basicInfo.apiId).order_by(
                        'index')
                    for item_extract in obj_db_ApiExtract:
                        extract.append({
                            'index': item_extract.index,
                            'key': item_extract.key,
                            'value': item_extract.value,
                            'remarks': item_extract.remarks,
                            'state': True if item_extract.state else False,
                        })
                    # endregion
                    # region validate
                    obj_db_ApiValidate = db_ApiValidate.objects.filter(is_del=0, apiId_id=basicInfo.apiId).order_by(
                        'index')
                    for item_validate in obj_db_ApiValidate:
                        validate.append({
                            'index': item_validate.index,
                            'checkName': item_validate.checkName,
                            'validateType': item_validate.validateType,
                            'valueType': item_validate.valueType,
                            'expectedResults': item_validate.expectedResults,
                            'remarks': item_validate.remarks,
                            'state': True if item_validate.state else False,
                        })
                    # endregion
                    # region 前置操作
                    obj_db_ApiOperation = db_ApiOperation.objects.filter(
                        is_del=0, apiId_id=basicInfo.apiId, location='Pre').order_by('index')
                    for item_preOperation in obj_db_ApiOperation:
                        preOperation.append({
                            'index': item_preOperation.index,
                            'operationType': item_preOperation.operationType,
                            'methodsName': item_preOperation.methodsName,
                            'dataBase': item_preOperation.dataBaseId,
                            'sql': item_preOperation.sql,
                            'remarks': item_preOperation.remarks,
                            'state': True if item_preOperation.state else False,
                        })
                    # endregion
                    # region 后置操作
                    obj_db_ApiOperation = db_ApiOperation.objects.filter(
                        is_del=0, apiId_id=basicInfo.apiId, location='Rear').order_by('index')
                    for item_rearOperation in obj_db_ApiOperation:
                        rearOperation.append({
                            'index': item_rearOperation.index,
                            'operationType': item_rearOperation.operationType,
                            'methodsName': item_rearOperation.methodsName,
                            'dataBase': item_rearOperation.dataBaseId,
                            'sql': item_rearOperation.sql,
                            'remarks': item_rearOperation.remarks,
                            'state': True if item_rearOperation.state else False,
                        })
                    # endregion
                    # endregion
                    obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(is_del=0, apiId_id=basicInfo.apiId)
                    pushTo = [i.uid_id for i in obj_db_ApiAssociatedUser]
                    oldData = {
                        'basicInfo': {
                            'apiId': basicInfo.apiId,
                            'proId': obj_db_ApiBaseData[0].pid_id,
                            'pageId': obj_db_ApiBaseData[0].page_id,
                            'funId': obj_db_ApiBaseData[0].fun_id,
                            'environmentId': obj_db_ApiBaseData[0].environment_id,
                            'apiName': obj_db_ApiBaseData[0].apiName,
                            'apiState': obj_db_ApiBaseData[0].apiState,
                            'assignedUserId': obj_db_ApiBaseData[0].uid_id,
                            'pushTo': pushTo,
                        },
                        'apiInfo': {
                            'requestType': obj_db_ApiBaseData[0].requestType,
                            'requestUrl': obj_db_ApiBaseData[0].requestUrl,
                            'request': {
                                'headers': headers,
                                'params': params,
                                'body': {
                                    'requestSaveType': obj_db_ApiBaseData[0].bodyRequestSaveType,
                                    'bodyData': bodyData
                                },
                                'extract': extract,
                                'validate': validate,
                                'preOperation': preOperation,
                                'rearOperation': rearOperation,
                            }
                        },
                        'cuid': obj_db_ApiBaseData[0].cuid
                    }
                    # endregion
                    operationInfoId = cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Edit',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        cls_FindTable.get_page_name(basicInfo.pageId),
                        cls_FindTable.get_fun_name(basicInfo.funId),
                        userId,
                        f'【修改接口】 ID{obj_db_ApiBaseData[0].id}:{obj_db_ApiBaseData[0].apiName}',
                        CUFront=oldData, CURear=responseData
                    )
                    # region 创建系统级别的工单
                    save_db_WorkorderManagement = db_WorkorderManagement.objects.create(
                        sysType='API', pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        workSource=1, workType='Edit', workState=0, workName=basicInfo.apiName,
                        message=f"{oldData}\n\n{responseData}",
                        uid_id=userId,
                        cuid=userId,
                        is_del=0,
                    )
                    # 创建工单生命周期
                    db_WorkLifeCycle.objects.create(
                        work_id=save_db_WorkorderManagement.id, workState=1, operationType='Add',
                        operationInfo=None, uid_id=userId, is_del=0,
                    )
                    # endregion
                    # endregion
                    # region 删除 各类原数据
                    db_ApiHeaders.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiParams.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiBody.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiExtract.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiValidate.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiOperation.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiAssociatedUser.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    # endregion
                    # region 更新基本信息
                    obj_db_ApiBaseData.update(
                        pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        apiName=basicInfo.apiName, environment_id=basicInfo.environmentId, apiState=basicInfo.apiState,
                        requestType=apiInfo.requestType, requestUrl=apiInfo.requestUrl._object_maker__data,
                        requestUrlRadio=requestUrlRadio,
                        requestParamsType='Body' if apiInfo.request.body.requestSaveType == 'none' else requestParamsType,
                        bodyRequestSaveType=apiInfo.request.body.requestSaveType,
                        uid_id=assignedUserId, cuid=userId, is_del=0, updateTime=cls_Common.get_date_time()
                    )
                    product_list_to_insert = list()
                    for item_userId in basicInfo.pushTo:
                        product_list_to_insert.append(db_ApiAssociatedUser(
                            apiId_id=basicInfo.apiId,
                            opertateInfo_id=operationInfoId,
                            uid_id=item_userId[1],
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiAssociatedUser.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 添加历史恢复
                    db_ApiHistory.objects.create(
                        pid_id=basicInfo.proId,
                        page_id=basicInfo.pageId,
                        fun_id=basicInfo.funId,
                        api_id=basicInfo.apiId,
                        apiName=oldData['basicInfo']['apiName'],
                        operationType='Edit',
                        restoreData=oldData,
                        onlyCode=historyCode,
                    )
                    # endregion
                    # region Headers
                    product_list_to_insert = list()
                    for item_headers in apiInfo.request.headers:
                        product_list_to_insert.append(db_ApiHeaders(
                            apiId_id=basicInfo.apiId,
                            index=item_headers.index,
                            key=item_headers.key,
                            value=item_headers.value,
                            remarks=item_headers.remarks,
                            state=1 if item_headers.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiHeaders.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Params
                    product_list_to_insert = list()
                    for item_params in apiInfo.request.params:
                        product_list_to_insert.append(db_ApiParams(
                            apiId_id=basicInfo.apiId,
                            index=item_params.index,
                            key=item_params.key,
                            value=item_params.value,
                            remarks=item_params.remarks,
                            state=1 if item_params.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiParams.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Body
                    if apiInfo.request.body.requestSaveType == 'form-data':
                        product_list_to_insert = list()
                        for item_body in apiInfo.request.body.formData:
                            product_list_to_insert.append(db_ApiBody(
                                apiId_id=basicInfo.apiId,
                                index=item_body.index,
                                key=item_body.key,
                                value=item_body.value,
                                remarks=item_body.remarks,
                                state=1 if item_body.state else 0,
                                is_del=0,
                                historyCode=historyCode)
                            )
                        db_ApiBody.objects.bulk_create(product_list_to_insert)
                    elif apiInfo.request.body.requestSaveType == 'raw':
                        db_ApiBody.objects.create(
                            apiId_id=basicInfo.apiId,
                            index=0,
                            key=None,
                            value=apiInfo.request.body.raw,
                            state=1,
                            is_del=0,
                            historyCode=historyCode
                        )
                    # file 之后在做
                    # endregion
                    # region Extract
                    product_list_to_insert = list()
                    for item_extract in apiInfo.request.extract:
                        product_list_to_insert.append(db_ApiExtract(
                            apiId_id=basicInfo.apiId,
                            index=item_extract.index,
                            key=item_extract.key,
                            value=item_extract.value,
                            remarks=item_extract.remarks,
                            state=1 if item_extract.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiExtract.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Validate
                    product_list_to_insert = list()
                    for item_validate in apiInfo.request.validate:
                        product_list_to_insert.append(db_ApiValidate(
                            apiId_id=basicInfo.apiId,
                            index=item_validate.index,
                            checkName=item_validate.checkName,
                            validateType=item_validate.validateType,
                            valueType=item_validate.valueType,
                            expectedResults=item_validate.expectedResults,
                            remarks=item_validate.remarks,
                            state=1 if item_validate.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiValidate.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 前置
                    product_list_to_insert = list()
                    for item_preOperation in apiInfo.request.preOperation:
                        product_list_to_insert.append(db_ApiOperation(
                            apiId_id=basicInfo.apiId,
                            index=item_preOperation.index,
                            location='Pre',
                            operationType=item_preOperation.operationType,
                            methodsName=item_preOperation.methodsName,
                            dataBaseId=item_preOperation.dataBase,
                            sql=item_preOperation.sql,
                            remarks=item_preOperation.remarks,
                            state=1 if item_preOperation.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 后置
                    product_list_to_insert = list()
                    for item_rearOperation in apiInfo.request.rearOperation:
                        product_list_to_insert.append(db_ApiOperation(
                            apiId_id=basicInfo.apiId,
                            index=item_rearOperation.index,
                            location='Rear',
                            operationType=item_rearOperation.operationType,
                            methodsName=item_rearOperation.methodsName,
                            dataBaseId=item_rearOperation.dataBase,
                            sql=item_rearOperation.sql,
                            remarks=item_rearOperation.remarks,
                            state=1 if item_rearOperation.state else 0,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 创建被关联用户的新增提醒
                    obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(
                        is_del=0, apiId_id=basicInfo.apiId)
                    for item_associatedUser in obj_db_ApiAssociatedUser:
                        db_WorkBindPushToUsers.objects.create(
                            work_id=save_db_WorkorderManagement.id,
                            uid_id=item_associatedUser.uid_id,
                            is_del=0
                        )
                        cls_Logging.push_to_user(operationInfoId, item_associatedUser.uid_id)
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'数据修改失败:{e}'
            else:
                response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找当前接口数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        apiId = request.POST['apiId']
        historyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'delete_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=apiId)
        if obj_db_ApiBaseData.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加历史恢复
                    db_ApiHistory.objects.create(
                        pid_id=obj_db_ApiBaseData[0].pid_id,
                        page_id=obj_db_ApiBaseData[0].page_id,
                        fun_id=obj_db_ApiBaseData[0].fun_id,
                        api_id=apiId,
                        apiName=obj_db_ApiBaseData[0].apiName,
                        operationType='Delete',
                        restoreData=None,
                        onlyCode=historyCode,
                    )
                    # endregion
                    # region 删除关联信息
                    obj_db_ApiBaseData.update(is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId)
                    db_ApiAssociatedUser.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time(), historyCode=historyCode)
                    db_ApiHeaders.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time(), historyCode=historyCode)
                    db_ApiParams.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time(), historyCode=historyCode)
                    db_ApiBody.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time(), historyCode=historyCode)
                    db_ApiExtract.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time(), historyCode=historyCode)
                    db_ApiValidate.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time(), historyCode=historyCode)
                    db_ApiOperation.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time(), historyCode=historyCode)
                    # endregion
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Delete',
                        cls_FindTable.get_pro_name(obj_db_ApiBaseData[0].pid_id),
                        cls_FindTable.get_page_name(obj_db_ApiBaseData[0].page_id),
                        cls_FindTable.get_fun_name(obj_db_ApiBaseData[0].fun_id),
                        userId,
                        f'【删除接口】 ID:{apiId}:{obj_db_ApiBaseData[0].apiName}',
                        CUFront=json.dumps(request.POST)
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'数据删除失败:{e}'
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前接口数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_data(request):
    response = {}
    headers = []
    params = []
    body = []
    extract = []
    validate = []
    preOperation = []  # 前置操作
    rearOperation = []  # 后置操作
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        apiId = objData.apiId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'load_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, id=apiId)
        if obj_db_ApiBaseData.exists():
            # region 基本信息
            roleId = cls_FindTable.get_roleId(obj_db_ApiBaseData[0].uid_id)
            pushTo = []
            obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(is_del=0, apiId_id=apiId)
            for item_associateUser in obj_db_ApiAssociatedUser:
                pushTo.append([cls_FindTable.get_roleId(item_associateUser.uid_id), item_associateUser.uid_id])
            basicInfo = {
                'pageId': obj_db_ApiBaseData[0].page_id,
                'funId': obj_db_ApiBaseData[0].fun_id,
                'environmentId': obj_db_ApiBaseData[0].environment_id,
                'apiName': obj_db_ApiBaseData[0].apiName,
                'apiState': obj_db_ApiBaseData[0].apiState,
                'assignedUserId': [roleId, obj_db_ApiBaseData[0].uid_id],
                'pushTo': pushTo,
            }
            # endregion
            # region headers
            obj_db_ApiHeaders = db_ApiHeaders.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            for item_headers in obj_db_ApiHeaders:
                headers.append({
                    'index': item_headers.index,
                    'key': item_headers.key,
                    'value': item_headers.value,
                    'remarks': item_headers.remarks,
                    'state': True if item_headers.state else False,
                })
            # endregion
            # region params
            obj_db_ApiParams = db_ApiParams.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            for item_params in obj_db_ApiParams:
                params.append({
                    'index': item_params.index,
                    'key': item_params.key,
                    'value': item_params.value,
                    'remarks': item_params.remarks,
                    'state': True if item_params.state else False,
                })
            # endregion
            # region body
            bodyData = None
            obj_db_ApiBody = db_ApiBody.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            if obj_db_ApiBaseData[0].bodyRequestSaveType == 'form-data':
                for item_body in obj_db_ApiBody:
                    body.append({
                        'index': item_body.index,
                        'key': item_body.key,
                        'value': item_body.value,
                        'remarks': item_body.remarks,
                        'state': True if item_body.state else False,
                    })
                bodyData = body
            elif obj_db_ApiBaseData[0].bodyRequestSaveType == 'raw':
                bodyData = obj_db_ApiBody[0].value
            # endregion
            # region extract
            obj_db_ApiExtract = db_ApiExtract.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            for item_extract in obj_db_ApiExtract:
                extract.append({
                    'index': item_extract.index,
                    'key': item_extract.key,
                    'value': item_extract.value,
                    'remarks': item_extract.remarks,
                    'state': True if item_extract.state else False,
                })
            # endregion
            # region validate
            obj_db_ApiValidate = db_ApiValidate.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            for item_validate in obj_db_ApiValidate:
                validate.append({
                    'index': item_validate.index,
                    'checkName': item_validate.checkName,
                    'validateType': item_validate.validateType,
                    'valueType': item_validate.valueType,
                    'expectedResults': item_validate.expectedResults,
                    'remarks': item_validate.remarks,
                    'state': True if item_validate.state else False,
                })
            # endregion
            # region 前置操作
            obj_db_ApiOperation = db_ApiOperation.objects.filter(
                is_del=0, apiId_id=apiId, location='Pre').order_by('index')
            for item_preOperation in obj_db_ApiOperation:
                preOperation.append({
                    'index': item_preOperation.index,
                    'operationType': item_preOperation.operationType,
                    'methodsName': item_preOperation.methodsName,
                    'dataBase': item_preOperation.dataBaseId,
                    'sql': item_preOperation.sql,
                    'remarks': item_preOperation.remarks,
                    'state': True if item_preOperation.state else False,
                })
            # endregion
            # region 后置操作
            obj_db_ApiOperation = db_ApiOperation.objects.filter(
                is_del=0, apiId_id=apiId, location='Rear').order_by('index')
            for item_rearOperation in obj_db_ApiOperation:
                rearOperation.append({
                    'index': item_rearOperation.index,
                    'operationType': item_rearOperation.operationType,
                    'methodsName': item_rearOperation.methodsName,
                    'dataBase': item_rearOperation.dataBaseId,
                    'sql': item_rearOperation.sql,
                    'remarks': item_rearOperation.remarks,
                    'state': True if item_rearOperation.state else False,
                })
            # endregion
            # region apiInfo
            requestUrlRadio = obj_db_ApiBaseData[0].requestUrlRadio
            requestUrl = ast.literal_eval(obj_db_ApiBaseData[0].requestUrl)
            currentRequestUrl = requestUrl[f'url{requestUrlRadio}']
            apiInfo = {
                'requestType': obj_db_ApiBaseData[0].requestType,
                'requestUrlRadio': requestUrlRadio,
                'currentRequestUrl': currentRequestUrl,
                'requestUrl1': requestUrl['url1'],
                'requestUrl2': requestUrl['url2'],
                'requestUrl3': requestUrl['url3'],
                'request': {
                    'headers': headers,
                    'params': params,
                    'body': {
                        'requestSaveType': obj_db_ApiBaseData[0].bodyRequestSaveType,
                        'bodyData': bodyData
                    },
                    'extract': extract,
                    'validate': validate,
                    'preOperation': preOperation,
                    'rearOperation': rearOperation,
                }
            }
            # endregion

            response['basicInfo'] = basicInfo
            response['apiInfo'] = apiInfo
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = "未找到当前选择的接口数据,请刷新后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def send_request(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        apiId = request.POST['apiId']
        environmentId = request.POST['environmentId']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'request_api', errorMsg)
    else:
        cls_Logging.print_log('info', 'send_request', '-----------------------------start-----------------------------')
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=apiId)
        if obj_db_ApiBaseData.exists():
            # region 创建1级主报告
            createTestReport = cls_ApiReport.create_test_report(
                obj_db_ApiBaseData[0].pid_id,
                obj_db_ApiBaseData[0].apiName,
                'API', apiId, 1, userId
            )
            # endregion
            if createTestReport['state']:
                # region  创建2级报告
                testReportId = createTestReport['testReportId']
                queueId = cls_ApiReport.create_queue(
                    obj_db_ApiBaseData[0].pid_id, obj_db_ApiBaseData[0].page_id, obj_db_ApiBaseData[0].fun_id
                    , 'API', apiId, testReportId, userId)  # 创建队列
                apiName = obj_db_ApiBaseData[0].apiName
                createReportItems = cls_ApiReport.create_report_items(testReportId, apiId, apiName)
                if createReportItems['state']:
                    reportItemId = createReportItems['reportItemId']
                    cls_ApiReport.update_queue(queueId, 1, userId)
                    # 请求运行
                    response = cls_RequstOperation.run_request(
                        False, onlyCode, userId, apiId=apiId, environmentId=environmentId, reportItemId=reportItemId)
                    if response['state']:
                        response['statusCode'] = 2000
                    else:
                        response['errorMsg'] = response['errorMsg']
                    # 更新2级报告
                    cls_ApiReport.update_report_items(testReportId, reportItemId)
                    cls_ApiReport.update_queue(queueId, 2, userId)
                else:
                    response['errorMsg'] = createReportItems['errorMsg']
                # endregion
            else:
                response['errorMsg'] = createTestReport['errorMsg']
        else:
            response['errorMsg'] = '当前请求的接口不存在,请刷新后在重新尝试'
        cls_Logging.print_log('info', 'send_request', '-----------------------------END-----------------------------')
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 异步请求
def asynchronous_request(request):
    pass


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def send_test_request(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        responseData = json.loads(request.body)
        # 核心请求是字典类型,不可使用对象来传输
        # objData = cls_object_maker(responseData)
        onlyCode = cls_Common.generate_only_code()
        testSendData = responseData['testSendData']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'request_api', errorMsg)
    else:
        cls_Logging.print_log('info', 'send_request', '-----------------------------start-----------------------------')
        # 获取环境URl
        obj_db_PageEnvironment = db_PageEnvironment.objects.filter(id=testSendData['BasicInfo']['environmentId'])
        if obj_db_PageEnvironment.exists():
            environmentUrl = obj_db_PageEnvironment[0].environmentUrl
            request = cls_object_maker(testSendData['ApiInfo']['request'])
            requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
                request.params, request.body.formData, request.body.raw,
            )
            requestParamsType = 'Body' if testSendData['ApiInfo']['request']['body'][
                                              'requestSaveType'] == 'none' else requestParamsType
            bodyRequestType = testSendData['ApiInfo']['request']['body']['requestSaveType']
            if bodyRequestType == 'form-data':
                bodyData = testSendData['ApiInfo']['request']['body']['formData']
            elif bodyRequestType in ('json', 'raw'):
                bodyData = testSendData['ApiInfo']['request']['body']['raw']
            else:
                bodyData = []
            requestUrlRadio = testSendData["ApiInfo"]["requestUrlRadio"]
            requestUrl = testSendData["ApiInfo"]["requestUrl"][f'url{requestUrlRadio}']
            requestData = {
                'state': True,
                'proId': testSendData['BasicInfo']['proId'],
                'requestType': testSendData['ApiInfo']['requestType'],
                'requestUrl': f'{environmentUrl}{requestUrl}',
                'requestParamsType': requestParamsType,
                'bodyRequestType': bodyRequestType,
                'headersData': testSendData['ApiInfo']['request']['headers'],
                'paramsData': testSendData['ApiInfo']['request']['params'],
                'bodyData': bodyData,
                'extractData': testSendData['ApiInfo']['request']['extract'],
                'validateData': testSendData['ApiInfo']['request']['validate'],
                'PreOperation': testSendData['ApiInfo']['request']['preOperation'],
                'RearOperation': testSendData['ApiInfo']['request']['rearOperation'],
            }
            response = cls_RequstOperation.run_request(True, onlyCode, userId, requestData=requestData)
            if response['state']:
                response['statusCode'] = 2000
        else:
            response['errorMsg'] = f"没有找到当前环境ID的环境数据!"
        cls_Logging.print_log('info', 'send_request', '-----------------------------END-----------------------------')
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def copy_api(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])  # 当前操作者
        apiId = objData.apiId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'copy_api', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, id=apiId)
        if obj_db_ApiBaseData.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    operationInfoId = cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(obj_db_ApiBaseData[0].pid_id),
                        cls_FindTable.get_page_name(obj_db_ApiBaseData[0].page_id),
                        cls_FindTable.get_fun_name(obj_db_ApiBaseData[0].fun_id),
                        userId,
                        '【复制接口】', CUFront=f"ID:{apiId},{obj_db_ApiBaseData[0].apiName}"
                    )
                    # endregion
                    # region 保存基本信息
                    save_db_ApiBaseData = db_ApiBaseData.objects.create(
                        pid_id=obj_db_ApiBaseData[0].pid_id,
                        page_id=obj_db_ApiBaseData[0].page_id,
                        fun_id=obj_db_ApiBaseData[0].fun_id,
                        apiName=f"{obj_db_ApiBaseData[0].apiName}-副本{operationInfoId}",
                        environment_id=obj_db_ApiBaseData[0].environment_id,
                        apiState=obj_db_ApiBaseData[0].apiState,
                        requestType=obj_db_ApiBaseData[0].requestType,
                        requestUrl=obj_db_ApiBaseData[0].requestUrl,
                        requestParamsType=obj_db_ApiBaseData[0].requestParamsType,
                        bodyRequestSaveType=obj_db_ApiBaseData[0].bodyRequestSaveType,
                        uid_id=userId, cuid=userId, is_del=0,
                    )
                    obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_userId in obj_db_ApiAssociatedUser:
                        product_list_to_insert.append(db_ApiAssociatedUser(
                            apiId_id=save_db_ApiBaseData.id,
                            opertateInfo_id=item_userId.opertateInfo_id,
                            uid_id=item_userId.uid_id,
                            is_del=0)
                        )
                    db_ApiAssociatedUser.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Headers
                    obj_db_ApiHeaders = db_ApiHeaders.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_headers in obj_db_ApiHeaders:
                        product_list_to_insert.append(db_ApiHeaders(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_headers.index,
                            key=item_headers.key,
                            value=item_headers.value,
                            remarks=item_headers.remarks,
                            state=item_headers.state,
                            is_del=0)
                        )
                    db_ApiHeaders.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Params
                    obj_db_ApiParams = db_ApiParams.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_params in obj_db_ApiParams:
                        product_list_to_insert.append(db_ApiParams(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_params.index,
                            key=item_params.key,
                            value=item_params.value,
                            remarks=item_params.remarks,
                            state=item_params.state,
                            is_del=0)
                        )
                    db_ApiParams.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Body
                    obj_db_ApiBody = db_ApiBody.objects.filter(apiId_id=apiId, is_del=0)
                    if obj_db_ApiBaseData[0].bodyRequestSaveType == 'form-data':
                        product_list_to_insert = list()
                        for item_body in obj_db_ApiBody:
                            product_list_to_insert.append(db_ApiBody(
                                apiId_id=save_db_ApiBaseData.id,
                                index=item_body.index,
                                key=item_body.key,
                                value=item_body.value,
                                remarks=item_body.remarks,
                                state=item_body.state,
                                is_del=0)
                            )
                        db_ApiBody.objects.bulk_create(product_list_to_insert)
                    elif obj_db_ApiBaseData[0].bodyRequestSaveType == 'raw':
                        if obj_db_ApiBody.exists():
                            db_ApiBody.objects.create(
                                apiId_id=save_db_ApiBaseData.id,
                                index=0,
                                key=None,
                                value=obj_db_ApiBody[0].value,
                                state=1,
                                is_del=0
                            )
                    # file 之后在做
                    # endregion
                    # region Extract
                    obj_db_ApiExtract = db_ApiExtract.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_extract in obj_db_ApiExtract:
                        product_list_to_insert.append(db_ApiExtract(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_extract.index,
                            key=item_extract.key,
                            value=item_extract.value,
                            remarks=item_extract.remarks,
                            state=item_extract.state,
                            is_del=0)
                        )
                    db_ApiExtract.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Validate
                    obj_db_ApiValidate = db_ApiValidate.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_validate in obj_db_ApiValidate:
                        product_list_to_insert.append(db_ApiValidate(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_validate.index,
                            checkName=item_validate.checkName,
                            validateType=item_validate.validateType,
                            valueType=item_validate.valueType,
                            expectedResults=item_validate.expectedResults,
                            remarks=item_validate.remarks,
                            state=item_validate.state,
                            is_del=0)
                        )
                    db_ApiValidate.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 前后置
                    obj_db_ApiOperation = db_ApiOperation.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_preOperation in obj_db_ApiOperation:
                        product_list_to_insert.append(db_ApiOperation(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_preOperation.index,
                            location=item_preOperation.location,
                            operationType=item_preOperation.operationType,
                            methodsName=item_preOperation.methodsName,
                            dataBaseId=item_preOperation.dataBaseId,
                            sql=item_preOperation.sql,
                            remarks=item_preOperation.remarks,
                            state=item_preOperation.state,
                            is_del=0)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # # region 创建被关联用户的新增提醒
                    # obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(
                    #     is_del=0, apiId_id=save_db_ApiBaseData.id)
                    # for item_associatedUser in obj_db_ApiAssociatedUser:
                    #     cls_Logging.push_to_user(operationInfoId, item_associatedUser.uid_id)
                    # # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f"复制接口失败:{e}"
            else:
                response['statusCode'] = 2000
        else:
            response['errorMsg'] = "未找到当前选择的接口数据,请刷新后重新尝试!"
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
        apiId = objData.apiId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'select_history', errorMsg)
    else:
        if apiId:
            obj_db_ApiHistory = db_ApiHistory.objects.filter(api_id=apiId).order_by('-createTime')
        else:
            obj_db_ApiHistory = db_ApiHistory.objects.filter().order_by('-createTime')
        for i in obj_db_ApiHistory:
            if i.restoreData:
                restoreData = json.dumps(ast.literal_eval(i.restoreData),
                                         sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)
            else:
                restoreData = None
            dataList.append({
                'id': i.id,
                'pageName': i.page.pageName,
                'funName': i.fun.funName,
                'apiName': i.apiName,
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
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'restor_data', errorMsg)
    else:
        obj_db_ApiHistory = db_ApiHistory.objects.filter(id=historyId)
        if obj_db_ApiHistory.exists():
            historyCode = obj_db_ApiHistory[0].onlyCode
            # 恢复时是管理员或是 当前项目的创建人时才可恢复
            if is_admin or obj_db_ApiHistory[0].pid.cuid == userId:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        obj_db_ProManagement = db_ProManagement.objects.filter(is_del=0, id=obj_db_ApiHistory[0].pid_id)
                        if obj_db_ProManagement.exists():
                            obj_db_PageManagement = db_PageManagement.objects.filter(
                                is_del=0, id=obj_db_ApiHistory[0].page_id)
                            if obj_db_PageManagement.exists():
                                obj_db_FunManagement = db_FunManagement.objects.filter(
                                    is_del=0, id=obj_db_ApiHistory[0].fun_id)
                                if obj_db_FunManagement.exists():
                                    apiId = obj_db_ApiHistory[0].api_id
                                    restoreData = obj_db_ApiHistory[0].restoreData
                                    if obj_db_ApiHistory[0].operationType == "Edit":
                                        # 编辑的恢复 历史ID不起作用因为用json格式恢复的
                                        restoreData = ast.literal_eval(restoreData)
                                        # region 操作记录
                                        operationInfoId = cls_Logging.record_operation_info(
                                            'API', 'Manual', 3, 'Edit',
                                            cls_FindTable.get_pro_name(obj_db_ApiHistory[0].pid_id),
                                            cls_FindTable.get_page_name(obj_db_ApiHistory[0].page_id),
                                            cls_FindTable.get_fun_name(obj_db_ApiHistory[0].fun_id),
                                            userId,
                                            f'【恢复接口】 ID:{obj_db_ApiHistory[0].api_id}:'
                                            f'{obj_db_ApiHistory[0].apiName}',
                                        )
                                        # endregion
                                        # region 基本数据
                                        if restoreData['apiInfo']['request']['params']:
                                            requestParamsType = 'Params'
                                        else:
                                            requestParamsType = 'Body'
                                        requestSaveType = restoreData['apiInfo']['request']['body']['requestSaveType']
                                        db_ApiBaseData.objects.filter(id=apiId).update(
                                            pid_id=restoreData['basicInfo']['proId'],
                                            page_id=restoreData['basicInfo']['pageId'],
                                            fun_id=restoreData['basicInfo']['funId'],
                                            apiName=restoreData['basicInfo']['apiName'],
                                            environment_id=restoreData['basicInfo']['environmentId'],
                                            apiState=restoreData['basicInfo']['apiState'],
                                            requestType=restoreData['apiInfo']['requestType'],
                                            requestUrl=restoreData['apiInfo']['requestUrl'],
                                            requestParamsType='Body' if requestSaveType == 'none' else requestParamsType,
                                            bodyRequestSaveType=requestSaveType,
                                            uid_id=userId, cuid=restoreData['cuid'], is_del=0,
                                            updateTime=cls_Common.get_date_time()
                                        )
                                        # 添加关联to
                                        product_list_to_insert = list()
                                        for item_userId in restoreData['basicInfo']['pushTo']:
                                            product_list_to_insert.append(db_ApiAssociatedUser(
                                                apiId_id=apiId,
                                                opertateInfo_id=operationInfoId,
                                                uid_id=item_userId,
                                                is_del=0)
                                            )
                                        db_ApiAssociatedUser.objects.bulk_create(product_list_to_insert)
                                        # endregion
                                        # region Headers
                                        db_ApiHeaders.objects.filter(is_del=0, apiId_id=apiId).update(
                                            is_del=1, updateTime=cls_Common.get_date_time()
                                        )
                                        product_list_to_insert = list()
                                        for item_headers in restoreData['apiInfo']['request']['headers']:
                                            product_list_to_insert.append(db_ApiHeaders(
                                                apiId_id=apiId,
                                                index=item_headers['index'],
                                                key=item_headers['key'],
                                                value=item_headers['value'],
                                                remarks=item_headers['remarks'],
                                                state=1 if item_headers['state'] else 0,
                                                is_del=0,
                                                historyCode=historyCode)
                                            )
                                        db_ApiHeaders.objects.bulk_create(product_list_to_insert)
                                        # endregion
                                        # region Params
                                        db_ApiParams.objects.filter(is_del=0, apiId_id=apiId).update(
                                            is_del=1, updateTime=cls_Common.get_date_time()
                                        )
                                        product_list_to_insert = list()
                                        for item_params in restoreData['apiInfo']['request']['params']:
                                            product_list_to_insert.append(db_ApiParams(
                                                apiId_id=apiId,
                                                index=item_params['index'],
                                                key=item_params['key'],
                                                value=item_params['value'],
                                                remarks=item_params['remarks'],
                                                state=1 if item_params['state'] else 0,
                                                is_del=0,
                                                historyCode=historyCode)
                                            )
                                        db_ApiParams.objects.bulk_create(product_list_to_insert)
                                        # endregion
                                        # region Body
                                        db_ApiBody.objects.filter(is_del=0, apiId_id=apiId).update(
                                            is_del=1, updateTime=cls_Common.get_date_time()
                                        )
                                        if requestSaveType == 'form-data':
                                            product_list_to_insert = list()
                                            for item_body in restoreData['apiInfo']['request']['body']['bodyData']:
                                                product_list_to_insert.append(db_ApiBody(
                                                    apiId_id=apiId,
                                                    index=item_body['index'],
                                                    key=item_body['key'],
                                                    value=item_body['value'],
                                                    remarks=item_body['remarks'],
                                                    state=1 if item_body['state'] else 0,
                                                    is_del=0, historyCode=historyCode)
                                                )
                                            db_ApiBody.objects.bulk_create(product_list_to_insert)
                                        elif requestSaveType == 'raw':
                                            db_ApiBody.objects.create(
                                                apiId_id=apiId,
                                                index=0,
                                                key=None,
                                                value=restoreData['apiInfo']['request']['body']['bodyData'],
                                                state=1,
                                                is_del=0, historyCode=historyCode
                                            )
                                        # file 之后在做
                                        # endregion
                                        # region Extract
                                        db_ApiExtract.objects.filter(is_del=0, apiId_id=apiId).update(
                                            is_del=1, updateTime=cls_Common.get_date_time()
                                        )
                                        product_list_to_insert = list()
                                        for item_extract in restoreData['apiInfo']['request']['extract']:
                                            product_list_to_insert.append(db_ApiExtract(
                                                apiId_id=apiId,
                                                index=item_extract['index'],
                                                key=item_extract['key'],
                                                value=item_extract['value'],
                                                remarks=item_extract['remarks'],
                                                state=1 if item_extract['state'] else 0,
                                                is_del=0, historyCode=historyCode)
                                            )
                                        db_ApiExtract.objects.bulk_create(product_list_to_insert)
                                        # endregion
                                        # region Validate
                                        db_ApiValidate.objects.filter(is_del=0, apiId_id=apiId).update(
                                            is_del=1, updateTime=cls_Common.get_date_time()
                                        )
                                        product_list_to_insert = list()
                                        for item_validate in restoreData['apiInfo']['request']['validate']:
                                            product_list_to_insert.append(db_ApiValidate(
                                                apiId_id=apiId,
                                                index=item_validate['index'],
                                                checkName=item_validate['checkName'],
                                                validateType=item_validate['validateType'],
                                                valueType=item_validate['valueType'],
                                                expectedResults=item_validate['expectedResults'],
                                                remarks=item_validate['remarks'],
                                                state=1 if item_validate['state'] else 0,
                                                is_del=0, historyCode=historyCode)
                                            )
                                        db_ApiValidate.objects.bulk_create(product_list_to_insert)
                                        # endregion
                                        # region 前置
                                        db_ApiOperation.objects.filter(is_del=0, apiId_id=apiId).update(
                                            is_del=1, updateTime=cls_Common.get_date_time()
                                        )
                                        product_list_to_insert = list()
                                        for item_preOperation in restoreData['apiInfo']['request']['preOperation']:
                                            product_list_to_insert.append(db_ApiOperation(
                                                apiId_id=apiId,
                                                index=item_preOperation['index'],
                                                location='Pre',
                                                operationType=item_preOperation['operationType'],
                                                methodsName=item_preOperation['methodsName'],
                                                dataBaseId=item_preOperation['dataBase'],
                                                sql=item_preOperation['sql'],
                                                remarks=item_preOperation['remarks'],
                                                state=1 if item_preOperation['state'] else 0,
                                                is_del=0, historyCode=historyCode)
                                            )
                                        db_ApiOperation.objects.bulk_create(product_list_to_insert)
                                        # endregion
                                        # region 后置
                                        product_list_to_insert = list()
                                        for item_rearOperation in restoreData['apiInfo']['request']['rearOperation']:
                                            product_list_to_insert.append(db_ApiOperation(
                                                apiId_id=apiId,
                                                index=item_rearOperation['index'],
                                                location='Rear',
                                                operationType=item_rearOperation['operationType'],
                                                methodsName=item_rearOperation['methodsName'],
                                                dataBaseId=item_rearOperation['dataBase'],
                                                sql=item_rearOperation['sql'],
                                                remarks=item_rearOperation['remarks'],
                                                state=1 if item_rearOperation['state'] else 0,
                                                is_del=0, historyCode=historyCode)
                                            )
                                        db_ApiOperation.objects.bulk_create(product_list_to_insert)
                                        # endregion
                                    else:  # Delete
                                        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
                                            id=obj_db_ApiHistory[0].api_id)
                                        if obj_db_ApiBaseData.exists():
                                            obj_db_ApiBaseData.update(
                                                is_del=0, updateTime=cls_Common.get_date_time(), uid_id=userId
                                            )
                                            # region 删除关联信息
                                            db_ApiHeaders.objects.filter(is_del=0, apiId_id=apiId).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_ApiParams.objects.filter(is_del=0, apiId_id=apiId).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_ApiBody.objects.filter(is_del=0, apiId_id=apiId).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_ApiExtract.objects.filter(is_del=0, apiId_id=apiId).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_ApiValidate.objects.filter(is_del=0, apiId_id=apiId).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_ApiOperation.objects.filter(is_del=0, apiId_id=apiId).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            # endregion
                                            # region 恢复数据
                                            db_ApiAssociatedUser.objects.filter(historyCode=historyCode).update(
                                                is_del=0, updateTime=cls_Common.get_date_time())
                                            db_ApiHeaders.objects.filter(historyCode=historyCode).update(
                                                is_del=0, updateTime=cls_Common.get_date_time())
                                            db_ApiParams.objects.filter(historyCode=historyCode).update(
                                                is_del=0, updateTime=cls_Common.get_date_time())
                                            db_ApiBody.objects.filter(historyCode=historyCode).update(
                                                is_del=0, updateTime=cls_Common.get_date_time())
                                            db_ApiExtract.objects.filter(historyCode=historyCode).update(
                                                is_del=0, updateTime=cls_Common.get_date_time())
                                            db_ApiValidate.objects.filter(historyCode=historyCode).update(
                                                is_del=0, updateTime=cls_Common.get_date_time())
                                            db_ApiOperation.objects.filter(historyCode=historyCode).update(
                                                is_del=0, updateTime=cls_Common.get_date_time())
                                            # endregion
                                            # region 操作记录
                                            cls_Logging.record_operation_info(
                                                'API', 'Manual', 3, 'Update',
                                                cls_FindTable.get_pro_name(obj_db_ApiHistory[0].pid_id),
                                                cls_FindTable.get_page_name(obj_db_ApiHistory[0].page_id),
                                                cls_FindTable.get_fun_name(obj_db_ApiHistory[0].fun_id),
                                                userId,
                                                f'【恢复接口】 ID:{obj_db_ApiHistory[0].api_id}:'
                                                f'{obj_db_ApiHistory[0].apiName}',
                                            )
                                            # endregion
                                        else:
                                            response['errorMsg'] = "未找到当前可恢复的数据!"
                                else:
                                    response['errorMsg'] = f"当前恢复的数据上级所属功能不存在,恢复失败!"
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
