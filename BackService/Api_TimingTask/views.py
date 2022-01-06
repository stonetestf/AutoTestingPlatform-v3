from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q

import json
import ast

# Create your db here.
from Api_CaseMaintenance.models import CaseBaseData as db_CaseBaseData
from Api_TimingTask.models import ApiTimingTask as db_ApiTimingTask
from Api_TimingTask.models import ApiTimingTaskTestSet as db_ApiTimingTaskTestSet

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.TestReport import ApiReport

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
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
        taskName = objData.taskName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'select_data', errorMsg)
    else:
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        select_db_ApiTimingTask = obj_db_ApiTimingTask[minSize: maxSize]
        if taskName:
            obj_db_ApiTimingTask = obj_db_ApiTimingTask.filter(taskName__icontains=taskName)
            select_db_ApiTimingTask = obj_db_ApiTimingTask[minSize: maxSize]

        for i in select_db_ApiTimingTask:
            dataList.append({
                'id': i.id,
                'taskName': i.taskName,
                'timingConfig': i.timingConfig,
                'taskSetTotal': db_ApiTimingTaskTestSet.objects.filter(is_del=0, timingTask_id=i.id).count(),
                'remarks': i.remarks,
                'taskStatus': True if i.taskStatus == 1 else False,
                'lastReportTime': '',
                'lastReportStatus': '',
                'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
                'createUserName': cls_FindTable.get_userName(i.cuid),
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_ApiTimingTask.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def select_case_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        proId = objData.proId
        pageId = objData.pageId
        funId = objData.funId
        passCaseId = objData.passCaseId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'select_case_data', errorMsg)
    else:
        if passCaseId:
            splitCaseId = passCaseId.split(',')
            passCaseIdList = [i for i in splitCaseId]
            # 这里过滤掉已放在用例集中的用例
            obj_db_CaseBaseData = db_CaseBaseData.objects.filter(~Q(id__in=passCaseIdList), is_del=0, pid_id=proId)
        else:
            obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, pid_id=proId)
        if pageId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(page_id=pageId)
        if funId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(fun_id=funId)

        for i in obj_db_CaseBaseData:
            dataList.append({
                'id': i.id,
                'pageName': i.page.pageName,
                'funName': i.fun.funName,
                'caseName': i.caseName,
                'caseState': i.caseState,
                'testType': i.testType,
                "userName": f"{i.uid.userName}({i.uid.nickName})",
            })

        response['TableData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 效验接数据的完成性
def charm_task_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        basicInfo = objData.BasicInfo
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'charm_task_data', errorMsg)
    else:
        # region 验证基本信息
        # region 项目下名称
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(
            is_del=0, pid_id=basicInfo.proId, taskName=basicInfo.taskName
        )
        if obj_db_ApiTimingTask.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属项目下已有相同定时任务名称,请更改!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ApiTimingTask.exists():
                    if basicInfo.caseId == obj_db_ApiTimingTask[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属项目下已有相同定时任务名称,请更改!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 相同时间
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(timingConfig=basicInfo.timingConfig)
        if obj_db_ApiTimingTask.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属项目下已有相同定时任务时间配置,请更改!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ApiTimingTask.exists():
                    if basicInfo.caseId == obj_db_ApiTimingTask[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属项目下已有相同定时任务时间配置,请更改!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 时间配置
        try:
            timingConfig = basicInfo.timingConfig.split(' ')
            if len(timingConfig) != 5:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前时间配置错误:时间格式不满足条件5,例子:* * * * *,请更改!',
                    'updateTime': cls_Common.get_date_time()})
        except BaseException as e:
            dataList.append({
                'stepsName': '基本信息',
                'errorMsg': f'当前时间配置错误:{e},例子:* * * * *,请更改!',
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
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'data_save', errorMsg)
    else:
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(
            is_del=0, pid_id=basicInfo.proId, taskName=basicInfo.taskName, timingConfig=basicInfo.timingConfig
        )
        if obj_db_ApiTimingTask.exists():
            response['errorMsg'] = f'当前所属项目下已有相同定时任务名称或配置时间,请更改!'
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        None, None,
                        userId,
                        '【新增定时任务】', CUFront=responseData
                    )
                    # endregion
                    # region 保存基本信息
                    save_db_ApiTimingTask = db_ApiTimingTask.objects.create(
                        pid_id=basicInfo.proId, taskName=basicInfo.taskName, environment_id=basicInfo.environmentId,
                        timingConfig=basicInfo.timingConfig, priority=basicInfo.priorityId,remarks=basicInfo.remarks,
                        pushTo=basicInfo.pushTo, taskStatus=basicInfo.taskStatus, cuid=userId, uid_id=userId, is_del=0
                    )
                    # endregion
                    # region 测试集
                    for item_index, item_testSet in enumerate(testSet, 0):
                        db_ApiTimingTaskTestSet.objects.create(
                            timingTask_id=save_db_ApiTimingTask.id,
                            index=item_index,
                            case_id=item_testSet.id,
                            state=1 if item_testSet.state else 0,
                            uid_id=userId,
                            is_del=0
                        )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['statusCode'] = 2001
    return JsonResponse(response)

@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_task_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        taskId = objData.taskId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'load_task_data', errorMsg)
    else:
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(is_del=0, id=taskId)
        if obj_db_ApiTimingTask.exists():
            # region 基础信息
            basicInfo = {
                'taskName': obj_db_ApiTimingTask[0].taskName,
                'environmentId': obj_db_ApiTimingTask[0].environment_id,
                'timingConfig': obj_db_ApiTimingTask[0].timingConfig,
                'priorityId': obj_db_ApiTimingTask[0].priority,
                'taskStatus': obj_db_ApiTimingTask[0].taskStatus,
                'pushTo':ast.literal_eval(obj_db_ApiTimingTask[0].pushTo) if obj_db_ApiTimingTask[0].pushTo else [],
                'remarks':obj_db_ApiTimingTask[0].remarks,
            }
            # endregion
            # region 测试集
            testSet = []
            # obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, caseId_id=caseId)
            # for item_testSet in obj_db_CaseTestSet:
            #     settingParams = False
            #     synchronous = True if item_testSet.is_synchronous == 1 else False
            #     requestData = {
            #         'requestType': 'GET',
            #         'requestUrl': '',
            #         'headers': [],
            #         'params': [],
            #         'body': {
            #             'requestSaveType': 'form-data',
            #             'formData': [],
            #             'rawValue': '',
            #             'jsonValue': '',
            #             'deleteFileList': [],
            #         },
            #         'extract': [],
            #         'validate': [],
            #         'preOperation': [],
            #         'rearOperation': [],
            #     }
            #     obj_db_CaseApiBase = db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id)
            #     if obj_db_CaseApiBase.exists():
            #         requestData['requestType'] = obj_db_CaseApiBase[0].requestType
            #         requestData['requestUrl'] = obj_db_CaseApiBase[0].requestUrl
            #         requestData['body']['requestSaveType'] = obj_db_CaseApiBase[0].bodyRequestSaveType
            #         if obj_db_CaseApiBase[0].requestUrl:
            #             settingParams = True
            #         # region headers
            #         obj_db_CaseApiHeaders = db_CaseApiHeaders.objects.filter(
            #             is_del=0, testSet_id=item_testSet.id).order_by('index')
            #         for item_headers in obj_db_CaseApiHeaders:
            #             requestData['headers'].append({
            #                 'index': item_headers.index,
            #                 'state': True if item_headers.state == 1 else False,
            #                 'key': item_headers.key,
            #                 'value': item_headers.value,
            #                 'remarks': item_headers.remarks,
            #             })
            #         # endregion
            #         # region params
            #         obj_db_CaseApiParams = db_CaseApiParams.objects.filter(
            #             is_del=0, testSet_id=item_testSet.id).order_by('index')
            #         for item_params in obj_db_CaseApiParams:
            #             requestData['params'].append({
            #                 'index': item_params.index,
            #                 'state': True if item_params.state == 1 else False,
            #                 'key': item_params.key,
            #                 'value': item_params.value,
            #                 'remarks': item_params.remarks,
            #             })
            #         # endregion
            #         # region body
            #         obj_db_CaseApiBody = db_CaseApiBody.objects.filter(
            #             is_del=0, testSet_id=item_testSet.id).order_by('index')
            #         if obj_db_CaseApiBase[0].bodyRequestSaveType == 'form-data':
            #             for item_body in obj_db_CaseApiBody:
            #                 if item_body.paramsType == 'Text':
            #                     fileList = []
            #                 else:
            #                     splitStr = item_body.filePath.split('/')
            #                     name = splitStr[-1]
            #                     url = f"{settings.NGINX_SERVER}CaseFile/{caseId}/{item_testSet.id}/{name}"
            #                     fileList = [
            #                         {'name': name, 'url': url}
            #                     ]
            #                 requestData['body']['formData'].append({
            #                     'index': item_body.index,
            #                     'state': True if item_body.state == 1 else False,
            #                     'key': item_body.key,
            #                     'paramsType': item_body.paramsType,
            #                     'value': item_body.value,
            #                     'fileList': fileList,
            #                     'remarks': item_body.remarks,
            #                 })
            #         elif obj_db_CaseApiBase[0].bodyRequestSaveType == 'raw':
            #             requestData['body']['rawValue'] = obj_db_CaseApiBody[0].value
            #         elif obj_db_CaseApiBase[0].bodyRequestSaveType == 'json':
            #             requestData['body']['jsonValue'] = obj_db_CaseApiBody[0].value
            #         # endregion
            #         # region Extract
            #         obj_db_CaseApiExtract = db_CaseApiExtract.objects.filter(
            #             is_del=0, testSet_id=item_testSet.id).order_by('index')
            #         for item_extract in obj_db_CaseApiExtract:
            #             requestData['extract'].append({
            #                 'index': item_extract.index,
            #                 'state': True if item_extract.state == 1 else False,
            #                 'key': item_extract.key,
            #                 'value': item_extract.value,
            #                 'remarks': item_extract.remarks,
            #             })
            #         # endregion
            #         # region Validate
            #         obj_db_CaseApiValidate = db_CaseApiValidate.objects.filter(
            #             is_del=0, testSet_id=item_testSet.id).order_by('index')
            #         for item_validate in obj_db_CaseApiValidate:
            #             requestData['validate'].append({
            #                 'index': item_validate.index,
            #                 'state': True if item_validate.state == 1 else False,
            #                 'checkName': item_validate.checkName,
            #                 'validateType': item_validate.validateType,
            #                 'valueType': item_validate.valueType,
            #                 'expectedResults': item_validate.expectedResults,
            #                 'remarks': item_validate.remarks,
            #             })
            #         # endregion
            #         # region 前置操作
            #         obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
            #             is_del=0, testSet_id=item_testSet.id, location='Pre').order_by('index')
            #         for item_preOperation in obj_db_CaseApiOperation:
            #             requestData['preOperation'].append({
            #                 'id': item_preOperation.index,
            #                 'index': item_preOperation.index,
            #                 'state': True if item_preOperation.state == 1 else False,
            #                 'operationType': item_preOperation.operationType,
            #                 'methodsName': item_preOperation.methodsName,
            #                 'dataBase': item_preOperation.dataBaseId,
            #                 'sql': item_preOperation.sql,
            #                 'remarks': item_preOperation.remarks,
            #             })
            #         # endregion
            #         # region 后置操作
            #         obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
            #             is_del=0, testSet_id=item_testSet.id, location='Rear').order_by('index')
            #         for item_rearOperation in obj_db_CaseApiOperation:
            #             requestData['rearOperation'].append({
            #                 'id': item_rearOperation.index,
            #                 'index': item_rearOperation.index,
            #                 'state': True if item_rearOperation.state == 1 else False,
            #                 'operationType': item_rearOperation.operationType,
            #                 'methodsName': item_rearOperation.methodsName,
            #                 'dataBase': item_rearOperation.dataBaseId,
            #                 'sql': item_rearOperation.sql,
            #                 'remarks': item_rearOperation.remarks,
            #             })
            #         # endregion
            #     obj_db_ApiDynamic = db_ApiDynamic.objects.filter(
            #         case_id=caseId, apiId_id=item_testSet.apiId_id, is_del=0, is_read=0)
            #     # 0 无更变、1 已更变、2 已知晓
            #     if obj_db_ApiDynamic.exists():
            #         if synchronous:  # 只对开启同步功能的接口 提示接口动态，未开始同步的接口因为是独立的参数可不提醒
            #             apidynamic = 1
            #         else:
            #             apidynamic = 0
            #     else:
            #         apidynamic = 0
            #     testSet.append({
            #         'id': item_testSet.pluralIntId,
            #         'apiId': item_testSet.apiId_id,
            #         'state': True if item_testSet.state == 1 else False,
            #         'apiName': item_testSet.apiId.apiName,
            #         'apiState': item_testSet.apiId.apiState,
            #         'testName': item_testSet.testName,
            #         'is_synchronous': synchronous,
            #         'settingParams': settingParams,
            #         'apidynamic': apidynamic,
            #         'request': requestData,
            #     })
            # endregion
            response['dataTable'] = {
                'basicInfo': basicInfo,
                'testSet': testSet,
            }
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = "当前选择的数据不存在,请刷新后在重新尝试!"
    return JsonResponse(response)
