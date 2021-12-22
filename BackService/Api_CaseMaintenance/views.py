from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData
from Api_IntMaintenance.models import ApiHeaders as db_ApiHeaders
from Api_IntMaintenance.models import ApiParams as db_ApiParams
from Api_IntMaintenance.models import ApiBody as db_ApiBody

from Api_IntMaintenance.models import ApiOperation as db_ApiOperation

from Api_CaseMaintenance.models import CaseBaseData as db_CaseBaseData
from Api_CaseMaintenance.models import CaseTestSet as db_CaseTestSet
from Api_CaseMaintenance.models import CaseApiBase as db_CaseApiBase
from Api_CaseMaintenance.models import CaseApiHeaders as db_CaseApiHeaders
from Api_CaseMaintenance.models import CaseApiParams as db_CaseApiParams
from Api_CaseMaintenance.models import CaseApiBody as db_CaseApiBody
from Api_CaseMaintenance.models import CaseApiExtract as db_CaseApiExtract
from Api_CaseMaintenance.models import CaseApiValidate as db_CaseApiValidate
from Api_CaseMaintenance.models import CaseApiOperation as db_CaseApiOperation

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

        proId = objData.proId
        pageId = objData.pageId
        funId = objData.funId
        labelId = objData.labelId
        caseState = objData.caseState
        caseName = objData.caseName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'select_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        select_db_CaseBaseData = obj_db_CaseBaseData[minSize: maxSize]
        if pageId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(page_id=pageId)
            select_db_CaseBaseData = obj_db_CaseBaseData[minSize: maxSize]
        if funId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(fun_id=funId)
            select_db_CaseBaseData = obj_db_CaseBaseData[minSize: maxSize]
        if labelId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(label=labelId)
            select_db_CaseBaseData = obj_db_CaseBaseData[minSize: maxSize]
        if caseState:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(caseState=caseState)
            select_db_CaseBaseData = obj_db_CaseBaseData[minSize: maxSize]
        if caseName:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(caseName__icontains=caseName)
            select_db_CaseBaseData = obj_db_CaseBaseData[minSize: maxSize]

        for i in select_db_CaseBaseData:
            dataList.append({
                'id': i.id,
                'priority': i.priority,
                'testType': i.testType,
                'caseName': i.caseName,
                'pageName': i.page.pageName,
                'funName': i.fun.funName,
                'labelId': i.label,
                'caseState': i.caseState,
                'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                'userName': i.uid.userName,
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_CaseBaseData.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_data(request):
    response = {}
    headers = []
    params = []
    body = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        # if '-' in objData.apiId:
        #     apiId = objData.apiId.split('-')[0]
        # else:
        apiId = objData.apiId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'load_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, id=apiId)
        if obj_db_ApiBaseData.exists():
            requestType = obj_db_ApiBaseData[0].requestType
            requestUrlRadio = obj_db_ApiBaseData[0].requestUrlRadio
            requestUrl = ast.literal_eval(obj_db_ApiBaseData[0].requestUrl)[f'url{requestUrlRadio}']
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
            requestSaveType = obj_db_ApiBaseData[0].bodyRequestSaveType
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

            apiInfo = {
                'requestType': requestType,
                'requestUrl': requestUrl,
                'request': {
                    'headers': headers,
                    'params': params,
                    'body': {
                        'requestSaveType': requestSaveType,
                        'bodyData': bodyData
                    },
                }
            }

            response['apiInfo'] = apiInfo
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = "未找到当前选择的接口数据,请刷新后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 效验接用例数据的完成性
def charm_case_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        basicInfo = objData.BasicInfo
        testSet = objData.TestSet
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'charm_case_data', errorMsg)
    else:
        # region 验证基本信息
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(
            is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
            label=basicInfo.labelId, testType=basicInfo.testType, caseName=basicInfo.caseName
        )
        if obj_db_CaseBaseData.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属功能及同标签同类型下已有相同用例名称,请更改!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_CaseBaseData.exists():
                    if basicInfo.caseId == obj_db_CaseBaseData[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属功能及同标签同类型下已有相同用例名称,请更改!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证测试集
        for index_testSet, item_testSet in enumerate(testSet, 1):
            # region 验证 headers
            if item_testSet.request.headers:
                for index, item_headers in enumerate(item_testSet.request.headers, 1):
                    if item_headers.state:
                        if not item_headers.key:
                            dataList.append({
                                'stepsName': f'接口信息-Headers',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:参数名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 params
            if item_testSet.request.params:
                for index, item_params in enumerate(item_testSet.request.params, 1):
                    if item_params.state:
                        if not item_params.key:
                            dataList.append({
                                'stepsName': '接口信息-Params',
                                'errorMsg': f'测试集(顺序:{index_testSet}):{index_testSet}):第{index}行:参数名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 body
            if item_testSet.request.body.requestSaveType == 'form-data':
                for index, item_body in enumerate(item_testSet.request.body.formData, 1):
                    if item_body.state:
                        if not item_body.key:
                            dataList.append({
                                'stepsName': '接口信息-Body',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:参数名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 提取
            if item_testSet.request.extract:
                for index, item_extract in enumerate(item_testSet.request.extract, 1):
                    if item_extract.state:
                        if not item_extract.key:
                            dataList.append({
                                'stepsName': '接口信息-Extract',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:变量名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_extract.value:
                            dataList.append({
                                'stepsName': '接口信息-Extract',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:提取表达式不可为空!',
                                'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 断言
            if item_testSet.request.validate:
                for index, item_validate in enumerate(item_testSet.request.validate, 1):
                    if item_validate.state:
                        if not item_validate.checkName:
                            dataList.append({
                                'stepsName': '接口信息-Validate',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行,提取变量名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_validate.validateType:
                            dataList.append({
                                'stepsName': '接口信息-Validate',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行,断言类型不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_validate.valueType:
                            dataList.append({
                                'stepsName': '接口信息-Validate',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:断言值类型不可为空!',
                                'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 前置操作
            if item_testSet.request.preOperation:
                for index, item_preOperation in enumerate(item_testSet.request.preOperation, 1):
                    if item_preOperation.state:
                        if item_preOperation.operationType == 'Methods':
                            if not item_preOperation.methodsName:
                                dataList.append({
                                    'stepsName': '接口信息-前置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:函数方法名称不可为空!',
                                    'updateTime': cls_Common.get_date_time()})
                            if '(' not in item_preOperation.methodsName or ')' not in item_preOperation.methodsName:
                                dataList.append({
                                    'stepsName': '接口信息-前置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:函数方法名称未检测到 ()',
                                    'updateTime': cls_Common.get_date_time()})

                        elif item_preOperation.operationType == 'DataBase':
                            if not item_preOperation.dataBase:
                                dataList.append({
                                    'stepsName': '接口信息-前置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:当前没有选择需要执行的数据库!',
                                    'updateTime': cls_Common.get_date_time()})
                            if not item_preOperation.sql:
                                dataList.append({
                                    'stepsName': '接口信息-前置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:请输入SQL语句!',
                                    'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 后置操作
            if item_testSet.request.rearOperation:
                for index, item_rearOperation in enumerate(item_testSet.request.rearOperation, 1):
                    if item_rearOperation.state:
                        if item_rearOperation.operationType == 'Methods':
                            if not item_rearOperation.methodsName:
                                dataList.append({
                                    'stepsName': '接口信息-后置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:函数方法名称不可为空!',
                                    'updateTime': cls_Common.get_date_time()})
                            if '(' not in item_rearOperation.methodsName or ')' not in item_rearOperation.methodsName:
                                dataList.append({
                                    'stepsName': '接口信息-后置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:函数方法名称未检测到 ()',
                                    'updateTime': cls_Common.get_date_time()})
                        elif item_rearOperation.operationType == 'DataBase':
                            if not item_rearOperation.dataBase:
                                dataList.append({
                                    'stepsName': '接口信息-后置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:当前没有选择需要执行的数据库!',
                                    'updateTime': cls_Common.get_date_time()})
                            if not item_rearOperation.sql:
                                dataList.append({
                                    'stepsName': '接口信息-后置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:请输入SQL语句!',
                                    'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证params 和body 至少有1个有参数
            if not item_testSet.request.params and \
                    not item_testSet.request.body.formData and \
                    not item_testSet.request.body.rawValue and not item_testSet.request.body.requestSaveType == 'none':
                dataList.append({
                    'stepsName': '接口信息-参数请求',
                    'errorMsg': f'测试集(顺序:{index_testSet}):不可创建空参数请求,Params或Body请求中至少有1个不可为空!',
                    'updateTime': cls_Common.get_date_time()})
            # endregion
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
        testSet = objData.TestSet
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'data_save', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(
            is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
            label=basicInfo.labelId, testType=basicInfo.testType, caseName=basicInfo.caseName
        )
        if obj_db_CaseBaseData.exists():
            response['errorMsg'] = f'当前所属功能及同标签同类型下已有相同用例名称,请更改!'
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        cls_FindTable.get_page_name(basicInfo.pageId),
                        cls_FindTable.get_fun_name(basicInfo.funId),
                        userId,
                        '【新增用例】', CUFront=responseData
                    )
                    # endregion
                    # region 保存基本信息
                    save_db_CaseBaseData = db_CaseBaseData.objects.create(
                        pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        environmentId_id=basicInfo.environmentId, testType=basicInfo.testType,
                        label=basicInfo.labelId, priority=basicInfo.priorityId, caseName=basicInfo.caseName,
                        caseState=basicInfo.caseState, cuid=userId, uid_id=userId, is_del=0
                    )
                    # endregion
                    # region 测试集
                    for item_index, item_testSet in enumerate(testSet, 0):
                        pluralIntId = item_testSet.apiId
                        apiId = pluralIntId.split('-')[0]
                        save_db_CaseTestSet = db_CaseTestSet.objects.create(
                            caseId_id=save_db_CaseBaseData.id,
                            index=item_index,
                            apiId_id=apiId,
                            pluralIntId=pluralIntId,
                            testName=item_testSet.testName,
                            is_synchronous=1 if item_testSet.is_synchronous else 0,
                            state=1 if item_testSet.state else 0,
                            uid_id=userId,
                            is_del=0
                        )
                        # region 请求基本数据
                        headers = item_testSet.request.headers
                        params = item_testSet.request.params
                        bodyRequestSaveType = item_testSet.request.body.requestSaveType
                        bodyFormData = item_testSet.request.body.formData
                        bodyRawValue = item_testSet.request.body.rawValue
                        extract = item_testSet.request.extract
                        validate = item_testSet.request.validate
                        preOperation = item_testSet.request.preOperation
                        rearOperation = item_testSet.request.rearOperation

                        requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
                            params, bodyFormData, bodyRawValue
                        )
                        db_CaseApiBase.objects.create(
                            testSet_id=save_db_CaseTestSet.id,
                            requestType=item_testSet.request.requestType,
                            requestUrl=item_testSet.request.requestUrl,
                            requestParamsType=requestParamsType,
                            bodyRequestSaveType=bodyRequestSaveType,
                            is_del=0
                        )
                        # endregion
                        # region Headers
                        product_list_to_insert = list()
                        for item_headers in headers:
                            product_list_to_insert.append(db_CaseApiHeaders(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_headers.index,
                                key=item_headers.key,
                                value=item_headers.value,
                                remarks=item_headers.remarks,
                                state=1 if item_headers.state else 0,
                                is_del=0)
                            )
                        db_CaseApiHeaders.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Params
                        product_list_to_insert = list()
                        for item_params in params:
                            product_list_to_insert.append(db_CaseApiParams(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_params.index,
                                key=item_params.key,
                                value=item_params.value,
                                remarks=item_params.remarks,
                                state=1 if item_params.state else 0,
                                is_del=0)
                            )
                        db_CaseApiParams.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Body
                        if bodyRequestSaveType == 'form-data':
                            product_list_to_insert = list()
                            for item_body in bodyFormData:
                                product_list_to_insert.append(db_CaseApiBody(
                                    testSet_id=save_db_CaseTestSet.id,
                                    index=item_body.index,
                                    key=item_body.key,
                                    value=item_body.value,
                                    remarks=item_body.remarks,
                                    state=1 if item_body.state else 0,
                                    is_del=0)
                                )
                            db_CaseApiBody.objects.bulk_create(product_list_to_insert)
                        elif bodyRequestSaveType == 'raw':
                            db_CaseApiBody.objects.create(
                                testSet_id=save_db_CaseTestSet.id,
                                index=0,
                                key=None,
                                value=bodyRawValue,
                                state=1,
                                is_del=0
                            )
                        # file 之后在做
                        # endregion
                        # region Extract
                        product_list_to_insert = list()
                        for item_extract in extract:
                            product_list_to_insert.append(db_CaseApiExtract(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_extract.index,
                                key=item_extract.key,
                                value=item_extract.value,
                                remarks=item_extract.remarks,
                                state=1 if item_extract.state else 0,
                                is_del=0, )
                            )
                        db_CaseApiExtract.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Validate
                        product_list_to_insert = list()
                        for item_validate in validate:
                            product_list_to_insert.append(db_CaseApiValidate(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_validate.index,
                                checkName=item_validate.checkName,
                                validateType=item_validate.validateType,
                                valueType=item_validate.valueType,
                                expectedResults=item_validate.expectedResults,
                                remarks=item_validate.remarks,
                                state=1 if item_validate.state else 0,
                                is_del=0, )
                            )
                        db_CaseApiValidate.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 前置
                        product_list_to_insert = list()
                        for item_preOperation in preOperation:
                            product_list_to_insert.append(db_CaseApiOperation(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_preOperation.index,
                                location='Pre',
                                operationType=item_preOperation.operationType,
                                methodsName=item_preOperation.methodsName,
                                dataBaseId=item_preOperation.dataBase,
                                sql=item_preOperation.sql,
                                remarks=item_preOperation.remarks,
                                state=1 if item_preOperation.state else 0,
                                is_del=0)
                            )
                        db_CaseApiOperation.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 后置
                        product_list_to_insert = list()
                        for item_rearOperation in rearOperation:
                            product_list_to_insert.append(db_CaseApiOperation(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_rearOperation.index,
                                location='Rear',
                                operationType=item_rearOperation.operationType,
                                methodsName=item_rearOperation.methodsName,
                                dataBaseId=item_rearOperation.dataBase,
                                sql=item_rearOperation.sql,
                                remarks=item_rearOperation.remarks,
                                state=1 if item_rearOperation.state else 0,
                                is_del=0, )
                            )
                        db_CaseApiOperation.objects.bulk_create(product_list_to_insert)
                        # endregion
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
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])  # 当前操作者
        basicInfo = objData.BasicInfo
        testSet = objData.TestSet
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'edit_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, id=basicInfo.caseId)
        if obj_db_CaseBaseData.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    # region 查询以前的数据
                    oldTestSet = []
                    obj_db_CaseTestSet = db_CaseTestSet.objects.filter(
                        is_del=0, caseId_id=basicInfo.caseId).order_by('index')
                    for item_testSet in obj_db_CaseTestSet:
                        settingParams = False
                        oldRequestData = {
                            'requestType': 'GET',
                            'requestUrl': '',
                            'headers': [],
                            'params': [],
                            'body': {
                                'requestSaveType': 'form-data',
                                'formData': [],
                                'rawValue': '',
                            },
                            'extract': [],
                            'validate': [],
                            'preOperation': [],
                            'rearOperation': [],
                        }
                        obj_db_CaseApiBase = db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id)
                        if obj_db_CaseApiBase.exists():
                            oldRequestData['requestType'] = obj_db_CaseApiBase[0].requestType
                            oldRequestData['requestUrl'] = obj_db_CaseApiBase[0].requestUrl
                            oldRequestData['body']['requestSaveType'] = obj_db_CaseApiBase[0].bodyRequestSaveType
                            if obj_db_CaseApiBase[0].requestUrl:
                                settingParams = True
                                # region headers
                                obj_db_CaseApiHeaders = db_CaseApiHeaders.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id).order_by('index')
                                for item_headers in obj_db_CaseApiHeaders:
                                    oldRequestData['headers'].append({
                                        'index': item_headers.index,
                                        'state': True if item_headers.state == 1 else False,
                                        'key': item_headers.key,
                                        'value': item_headers.value,
                                        'remarks': item_headers.remarks,
                                    })
                                # endregion
                                # region params
                                obj_db_CaseApiParams = db_CaseApiParams.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id).order_by('index')
                                for item_params in obj_db_CaseApiParams:
                                    oldRequestData['params'].append({
                                        'index': item_params.index,
                                        'state': True if item_params.state == 1 else False,
                                        'key': item_params.key,
                                        'value': item_params.value,
                                        'remarks': item_params.remarks,
                                    })
                                # endregion
                                # region body
                                obj_db_CaseApiBody = db_CaseApiBody.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id).order_by('index')
                                if obj_db_CaseApiBase[0].bodyRequestSaveType == 'form-data':
                                    for item_body in obj_db_CaseApiBody:
                                        oldRequestData['body']['formData'].append({
                                            'index': item_body.index,
                                            'state': True if item_body.state == 1 else False,
                                            'key': item_body.key,
                                            'value': item_body.value,
                                            'remarks': item_body.remarks,
                                        })
                                elif obj_db_CaseApiBase[0].bodyRequestSaveType == 'raw':
                                    oldRequestData['body']['rawValue'] = obj_db_CaseApiParams[0].value
                                # endregion
                                # region Extract
                                obj_db_CaseApiExtract = db_CaseApiExtract.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id).order_by('index')
                                for item_extract in obj_db_CaseApiExtract:
                                    oldRequestData['extract'].append({
                                        'index': item_extract.index,
                                        'state': True if item_extract.state == 1 else False,
                                        'key': item_extract.key,
                                        'value': item_extract.value,
                                        'remarks': item_extract.remarks,
                                    })
                                # endregion
                                # region Validate
                                obj_db_CaseApiValidate = db_CaseApiValidate.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id).order_by('index')
                                for item_validate in obj_db_CaseApiValidate:
                                    oldRequestData['validate'].append({
                                        'index': item_validate.index,
                                        'state': True if item_validate.state == 1 else False,
                                        'checkName': item_validate.checkName,
                                        'validateType': item_validate.validateType,
                                        'valueType': item_validate.valueType,
                                        'expectedResults': item_validate.expectedResults,
                                        'remarks': item_validate.remarks,
                                    })
                                # endregion
                                # region 前置操作
                                obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id, location='Pre').order_by('index')
                                for item_preOperation in obj_db_CaseApiOperation:
                                    oldRequestData['preOperation'].append({
                                        'id': item_preOperation.index,
                                        'index': item_preOperation.index,
                                        'state': True if item_preOperation.state == 1 else False,
                                        'operationType': item_preOperation.operationType,
                                        'methodsName': item_preOperation.methodsName,
                                        'dataBase': item_preOperation.dataBaseId,
                                        'sql': item_preOperation.sql,
                                        'remarks':item_preOperation.remarks,
                                    })
                                # endregion
                                # region 后置操作
                                obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id, location='Rear').order_by('index')
                                for item_rearOperation in obj_db_CaseApiOperation:
                                    oldRequestData['rearOperation'].append({
                                        'id': item_rearOperation.index,
                                        'index': item_rearOperation.index,
                                        'state': True if item_rearOperation.state == 1 else False,
                                        'operationType': item_rearOperation.operationType,
                                        'methodsName': item_rearOperation.methodsName,
                                        'dataBase': item_rearOperation.dataBaseId,
                                        'sql': item_rearOperation.sql,
                                        'remarks': item_rearOperation.remarks,
                                    })
                                # endregion
                        oldTestSet.append({
                            'apiId': item_testSet.apiId_id,
                            'state': True if item_testSet.state == 1 else False,
                            'apiName': item_testSet.apiId.apiName,
                            'apiState': item_testSet.apiId.apiState,
                            'testName': item_testSet.testName,
                            'is_synchronous': True if item_testSet.is_synchronous == 1 else False,
                            'settingParams': settingParams,
                            'request': oldRequestData
                        })
                    oldData = {
                        'basicInfo': {
                            'caseId': obj_db_CaseBaseData[0].id,
                            'proId': obj_db_CaseBaseData[0].pid_id,
                            'pageId': obj_db_CaseBaseData[0].page_id,
                            'funId': obj_db_CaseBaseData[0].fun_id,
                            'environmentId': obj_db_CaseBaseData[0].environmentId_id,
                            'priorityId': obj_db_CaseBaseData[0].priority,
                            'labelId': obj_db_CaseBaseData[0].label,
                            'testType': obj_db_CaseBaseData[0].testType,
                            'caseName': obj_db_CaseBaseData[0].caseName,
                            'caseState': obj_db_CaseBaseData[0].caseState,
                        },
                        'testSet': oldTestSet,

                    }
                    operationInfoId = cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Edit',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        cls_FindTable.get_page_name(basicInfo.pageId),
                        cls_FindTable.get_fun_name(basicInfo.funId),
                        userId,
                        f'【修改用例】 ID{obj_db_CaseBaseData[0].id}:{obj_db_CaseBaseData[0].caseName}',
                        CUFront=oldData, CURear=responseData
                    )

                    # endregion
                    # endregion
                    # region 删除 各类原数据
                    obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, caseId_id=basicInfo.caseId)
                    for item_testSet in obj_db_CaseTestSet:
                        db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiHeaders.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiParams.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiBody.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiExtract.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiValidate.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiOperation.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                    obj_db_CaseTestSet.update(is_del=1, updateTime=cls_Common.get_date_time(),uid_id=userId)
                    # endregion
                    # region 更新基本信息
                    db_CaseBaseData.objects.filter(is_del=0,id=basicInfo.caseId).update(
                        pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        environmentId_id=basicInfo.environmentId, testType=basicInfo.testType,
                        label=basicInfo.labelId, priority=basicInfo.priorityId, caseName=basicInfo.caseName,
                        caseState=basicInfo.caseState, uid_id=userId,
                    )
                    # endregion
                    # region 测试集
                    for item_index, item_testSet in enumerate(testSet, 0):
                        pluralIntId = item_testSet.apiId
                        apiId = pluralIntId.split('-')[0]
                        save_db_CaseTestSet = db_CaseTestSet.objects.create(
                            caseId_id=basicInfo.caseId,
                            index=item_index,
                            apiId_id=apiId,
                            pluralIntId=pluralIntId,
                            testName=item_testSet.testName,
                            is_synchronous=1 if item_testSet.is_synchronous else 0,
                            state=1 if item_testSet.state else 0,
                            uid_id=userId,
                            is_del=0
                        )
                        # region 请求基本数据
                        headers = item_testSet.request.headers
                        params = item_testSet.request.params
                        bodyRequestSaveType = item_testSet.request.body.requestSaveType
                        bodyFormData = item_testSet.request.body.formData
                        bodyRawValue = item_testSet.request.body.rawValue
                        extract = item_testSet.request.extract
                        validate = item_testSet.request.validate
                        preOperation = item_testSet.request.preOperation
                        rearOperation = item_testSet.request.rearOperation

                        requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
                            params, bodyFormData, bodyRawValue
                        )
                        db_CaseApiBase.objects.create(
                            testSet_id=save_db_CaseTestSet.id,
                            requestType=item_testSet.request.requestType,
                            requestUrl=item_testSet.request.requestUrl,
                            requestParamsType=requestParamsType,
                            bodyRequestSaveType=bodyRequestSaveType,
                            is_del=0
                        )
                        # endregion
                        # region Headers
                        product_list_to_insert = list()
                        for item_headers in headers:
                            product_list_to_insert.append(db_CaseApiHeaders(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_headers.index,
                                key=item_headers.key,
                                value=item_headers.value,
                                remarks=item_headers.remarks,
                                state=1 if item_headers.state else 0,
                                is_del=0)
                            )
                        db_CaseApiHeaders.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Params
                        product_list_to_insert = list()
                        for item_params in params:
                            product_list_to_insert.append(db_CaseApiParams(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_params.index,
                                key=item_params.key,
                                value=item_params.value,
                                remarks=item_params.remarks,
                                state=1 if item_params.state else 0,
                                is_del=0)
                            )
                        db_CaseApiParams.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Body
                        if bodyRequestSaveType == 'form-data':
                            product_list_to_insert = list()
                            for item_body in bodyFormData:
                                product_list_to_insert.append(db_CaseApiBody(
                                    testSet_id=save_db_CaseTestSet.id,
                                    index=item_body.index,
                                    key=item_body.key,
                                    value=item_body.value,
                                    remarks=item_body.remarks,
                                    state=1 if item_body.state else 0,
                                    is_del=0)
                                )
                            db_CaseApiBody.objects.bulk_create(product_list_to_insert)
                        elif bodyRequestSaveType == 'raw':
                            db_CaseApiBody.objects.create(
                                testSet_id=save_db_CaseTestSet.id,
                                index=0,
                                key=None,
                                value=bodyRawValue,
                                state=1,
                                is_del=0
                            )
                        # file 之后在做
                        # endregion
                        # region Extract
                        product_list_to_insert = list()
                        for item_extract in extract:
                            product_list_to_insert.append(db_CaseApiExtract(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_extract.index,
                                key=item_extract.key,
                                value=item_extract.value,
                                remarks=item_extract.remarks,
                                state=1 if item_extract.state else 0,
                                is_del=0, )
                            )
                        db_CaseApiExtract.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Validate
                        product_list_to_insert = list()
                        for item_validate in validate:
                            product_list_to_insert.append(db_CaseApiValidate(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_validate.index,
                                checkName=item_validate.checkName,
                                validateType=item_validate.validateType,
                                valueType=item_validate.valueType,
                                expectedResults=item_validate.expectedResults,
                                remarks=item_validate.remarks,
                                state=1 if item_validate.state else 0,
                                is_del=0, )
                            )
                        db_CaseApiValidate.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 前置
                        product_list_to_insert = list()
                        for item_preOperation in preOperation:
                            product_list_to_insert.append(db_CaseApiOperation(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_preOperation.index,
                                location='Pre',
                                operationType=item_preOperation.operationType,
                                methodsName=item_preOperation.methodsName,
                                dataBaseId=item_preOperation.dataBase,
                                sql=item_preOperation.sql,
                                remarks=item_preOperation.remarks,
                                state=1 if item_preOperation.state else 0,
                                is_del=0)
                            )
                        db_CaseApiOperation.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 后置
                        product_list_to_insert = list()
                        for item_rearOperation in rearOperation:
                            product_list_to_insert.append(db_CaseApiOperation(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_rearOperation.index,
                                location='Rear',
                                operationType=item_rearOperation.operationType,
                                methodsName=item_rearOperation.methodsName,
                                dataBaseId=item_rearOperation.dataBase,
                                sql=item_rearOperation.sql,
                                remarks=item_rearOperation.remarks,
                                state=1 if item_rearOperation.state else 0,
                                is_del=0, )
                            )
                        db_CaseApiOperation.objects.bulk_create(product_list_to_insert)
                        # endregion
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找到当前测试用例,请刷新后在重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        caseId = request.POST['caseId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'delete_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(id=caseId)
        if obj_db_CaseBaseData.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 删除关联信息
                    obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, caseId_id=caseId)
                    for item_testSet in obj_db_CaseTestSet:
                        db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiHeaders.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiParams.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiBody.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiExtract.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiValidate.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiOperation.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                    obj_db_CaseTestSet.update(is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId)
                    obj_db_CaseBaseData.update(is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId)
                    # endregion
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Delete',
                        cls_FindTable.get_pro_name(obj_db_CaseBaseData[0].pid_id),
                        cls_FindTable.get_page_name(obj_db_CaseBaseData[0].page_id),
                        cls_FindTable.get_fun_name(obj_db_CaseBaseData[0].fun_id),
                        userId,
                        f'【删除用例】 ID:{caseId}:{obj_db_CaseBaseData[0].caseName}',
                        CUFront=json.dumps(request.POST)
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'数据删除失败:{e}'
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前用例数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_case_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        caseId = objData.caseId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'load_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, id=caseId)
        if obj_db_CaseBaseData.exists():
            # region 基础信息
            basicInfo = {
                'pageId': obj_db_CaseBaseData[0].page_id,
                'funId': obj_db_CaseBaseData[0].fun_id,
                'environmentId': obj_db_CaseBaseData[0].environmentId_id,
                'testType': obj_db_CaseBaseData[0].testType,
                'labelId': obj_db_CaseBaseData[0].label,
                'priorityId': obj_db_CaseBaseData[0].priority,
                'caseName': obj_db_CaseBaseData[0].caseName,
                'caseState': obj_db_CaseBaseData[0].caseState,
            }
            # endregion
            # region 测试集
            testSet = []
            obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, caseId_id=caseId)
            for item_testSet in obj_db_CaseTestSet:
                settingParams = False
                requestData = {
                    'requestType': 'GET',
                    'requestUrl': '',
                    'headers': [],
                    'params': [],
                    'body': {
                        'requestSaveType': 'form-data',
                        'formData': [],
                        'rawValue': '',
                    },
                    'extract': [],
                    'validate': [],
                    'preOperation': [],
                    'rearOperation': [],
                }
                obj_db_CaseApiBase = db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id)
                if obj_db_CaseApiBase.exists():
                    requestData['requestType'] = obj_db_CaseApiBase[0].requestType
                    requestData['requestUrl'] = obj_db_CaseApiBase[0].requestUrl
                    requestData['body']['requestSaveType'] = obj_db_CaseApiBase[0].bodyRequestSaveType
                    if obj_db_CaseApiBase[0].requestUrl:
                        settingParams = True
                    # region headers
                    obj_db_CaseApiHeaders = db_CaseApiHeaders.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    for item_headers in obj_db_CaseApiHeaders:
                        requestData['headers'].append({
                            'index': item_headers.index,
                            'state': True if item_headers.state == 1 else False,
                            'key': item_headers.key,
                            'value': item_headers.value,
                            'remarks': item_headers.remarks,
                        })
                    # endregion
                    # region params
                    obj_db_CaseApiParams = db_CaseApiParams.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    for item_params in obj_db_CaseApiParams:
                        requestData['params'].append({
                            'index': item_params.index,
                            'state': True if item_params.state == 1 else False,
                            'key': item_params.key,
                            'value': item_params.value,
                            'remarks': item_params.remarks,
                        })
                    # endregion
                    # region body
                    obj_db_CaseApiBody = db_CaseApiBody.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    if obj_db_CaseApiBase[0].bodyRequestSaveType == 'form-data':
                        for item_body in obj_db_CaseApiBody:
                            requestData['body']['formData'].append({
                                'index': item_body.index,
                                'state': True if item_body.state == 1 else False,
                                'key': item_body.key,
                                'value': item_body.value,
                                'remarks': item_body.remarks,
                            })
                    elif obj_db_CaseApiBase[0].bodyRequestSaveType == 'raw':
                        requestData['body']['rawValue'] = obj_db_CaseApiParams[0].value
                    # endregion
                    # region Extract
                    obj_db_CaseApiExtract = db_CaseApiExtract.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    for item_extract in obj_db_CaseApiExtract:
                        requestData['extract'].append({
                            'index': item_extract.index,
                            'state': True if item_extract.state == 1 else False,
                            'key': item_extract.key,
                            'value': item_extract.value,
                            'remarks': item_extract.remarks,
                        })
                    # endregion
                    # region Validate
                    obj_db_CaseApiValidate = db_CaseApiValidate.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    for item_validate in obj_db_CaseApiValidate:
                        requestData['validate'].append({
                            'index': item_validate.index,
                            'state': True if item_validate.state == 1 else False,
                            'checkName': item_validate.checkName,
                            'validateType': item_validate.validateType,
                            'valueType': item_validate.valueType,
                            'expectedResults': item_validate.expectedResults,
                            'remarks': item_validate.remarks,
                        })
                    # endregion
                    # region 前置操作
                    obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
                        is_del=0, testSet_id=item_testSet.id, location='Pre').order_by('index')
                    for item_preOperation in obj_db_CaseApiOperation:
                        requestData['preOperation'].append({
                            'id': item_preOperation.index,
                            'index': item_preOperation.index,
                            'state': True if item_preOperation.state == 1 else False,
                            'operationType': item_preOperation.operationType,
                            'methodsName': item_preOperation.methodsName,
                            'dataBase': item_preOperation.dataBaseId,
                            'sql': item_preOperation.sql,
                            'remarks':item_preOperation.remarks,
                        })
                    # endregion
                    # region 后置操作
                    obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
                        is_del=0, testSet_id=item_testSet.id, location='Rear').order_by('index')
                    for item_rearOperation in obj_db_CaseApiOperation:
                        requestData['rearOperation'].append({
                            'id': item_rearOperation.index,
                            'index': item_rearOperation.index,
                            'state': True if item_rearOperation.state == 1 else False,
                            'operationType': item_rearOperation.operationType,
                            'methodsName': item_rearOperation.methodsName,
                            'dataBase': item_rearOperation.dataBaseId,
                            'sql': item_rearOperation.sql,
                            'remarks': item_rearOperation.remarks,
                        })
                    # endregion
                testSet.append({
                    'apiId': item_testSet.pluralIntId,
                    'state': True if item_testSet.state == 1 else False,
                    'apiName': item_testSet.apiId.apiName,
                    'apiState': item_testSet.apiId.apiState,
                    'testName': item_testSet.testName,
                    'is_synchronous': True if item_testSet.is_synchronous == 1 else False,
                    'settingParams': settingParams,
                    'request': requestData,
                })
            # endregion
            response['dataTable'] = {
                'basicInfo': basicInfo,
                'testSet': testSet,
            }
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = "当前选择的数据不存在,请刷新后在重新尝试!"
    return JsonResponse(response)
