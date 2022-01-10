from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
from dwebsocket.decorators import accept_websocket
from django.db.models import Q
from time import sleep
from django.conf import settings

import json
import ast

# Create your db here.
from Api_TimingTask.models import ApiTimingTask as db_ApiTimingTask
from Api_TestReport.models import ApiTestReport as db_ApiTestReport
from Api_TimingTask.models import ApiTimingTaskTestSet as db_ApiTimingTaskTestSet
from Api_BatchTask.models import ApiBatchTask as db_ApiBatchTask
from Api_BatchTask.models import ApiBatchTaskTestSet as db_ApiBatchTaskTestSet

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.Request import RequstOperation
from ClassData.TestReport import ApiReport
from ClassData.Redis import RedisHandle
from ClassData.FileOperations import FileOperations

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RequstOperation = RequstOperation()
cls_ApiReport = ApiReport()
cls_RedisHandle = RedisHandle()
cls_FileOperations = FileOperations()


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
        batchName = objData.batchName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_BatchTask', 'select_data', errorMsg)
    else:
        obj_db_ApiBatchTask = db_ApiBatchTask.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        select_db_ApiBatchTask = obj_db_ApiBatchTask[minSize: maxSize]
        if batchName:
            obj_db_ApiBatchTask = obj_db_ApiBatchTask.filter(batchName__icontains=batchName)
            select_db_ApiBatchTask = obj_db_ApiBatchTask[minSize: maxSize]

        for i in select_db_ApiBatchTask:
            obj_db_ApiTestReport = db_ApiTestReport.objects.filter(
                is_del=0, reportType='BATCH', taskId=i.id).order_by('-updateTime')
            if obj_db_ApiTestReport.exists():
                lastReportTime = obj_db_ApiTestReport[0].runningTime
                lastReportStatus = obj_db_ApiTestReport[0].reportStatus
            else:
                lastReportTime = ''
                lastReportStatus = ''
            # region 通过率
            obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, reportType='BATCH', taskId=i.id)
            passTotal = obj_db_ApiTestReport.filter(reportStatus='Pass').count()
            if obj_db_ApiTestReport.count() == 0:
                passRate = 0
            else:
                passRate = round(passTotal / obj_db_ApiTestReport.count() * 100, 2)
            # endregion
            dataList.append({
                'id': i.id,
                'batchName': i.batchName,
                'taskTotal': db_ApiBatchTaskTestSet.objects.filter(is_del=0, batchTask_id=i.id).count(),
                'remarks': i.remarks,
                'hookState': True if i.hookState == 1 else False,
                'lastReportTime': lastReportTime,
                'lastReportStatus': lastReportStatus,
                'passRate': passRate,
                'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
                'createUserName': cls_FindTable.get_userName(i.cuid),
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_ApiBatchTask.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 生成钩子ID
def create_hook_id(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_BatchTask', 'create_hook_id', errorMsg)
    else:
        response['hookId'] = cls_Common.generate_only_code()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def select_task_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        proId = objData.proId
        taskName = objData.taskName
        passTaskId = objData.passTaskId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_BatchTask', 'select_task_data', errorMsg)
    else:
        if passTaskId:
            splitTaskId = passTaskId.split(',')
            passTaskIdList = [i for i in splitTaskId]
            # 这里过滤掉已放在用例集中的用例
            obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(~Q(id__in=passTaskIdList), is_del=0, pid_id=proId)
        else:
            obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(is_del=0, pid_id=proId)
        if taskName:
            obj_db_ApiTimingTask = obj_db_ApiTimingTask.filter(taskName__icontains=taskName)

        for i in obj_db_ApiTimingTask:
            # region 通过率
            obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, reportType='TASK', taskId=i.id)
            passTotal = obj_db_ApiTestReport.filter(reportStatus='Pass').count()
            if obj_db_ApiTestReport.count() == 0:
                passRate = 0
            else:
                passRate = round(passTotal / obj_db_ApiTestReport.count() * 100, 2)
            # endregion
            dataList.append({
                'id': i.id,
                'taskName': i.taskName,
                'caseTotal': db_ApiTimingTaskTestSet.objects.filter(is_del=0, timingTask_id=i.id).count(),
                'taskState': True if i.taskStatus == 1 else False,
                'passRate': passRate,
                "userName": f"{i.uid.userName}({i.uid.nickName})",
                'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
            })

        response['TableData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 效验接数据的完成性
def charm_batch_data(request):
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
        cls_Logging.record_error_info('API', 'Api_BatchTask', 'charm_batch_data', errorMsg)
    else:
        # region 验证基本信息
        # region 项目下名称
        obj_db_ApiBatchTask = db_ApiBatchTask.objects.filter(
            is_del=0, pid_id=basicInfo.proId, batchName=basicInfo.batchName
        )
        if obj_db_ApiBatchTask.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属项目下已有相同批量任务名称,请更改!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ApiBatchTask.exists():
                    if basicInfo.taskId == obj_db_ApiBatchTask[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属项目下已有相同批量任务名称,请更改!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 相同钩子ID 可能性几乎很小
        obj_db_ApiBatchTask = db_ApiBatchTask.objects.filter(
            is_del=0, pid_id=basicInfo.proId, hookId=basicInfo.hookId
        )
        if obj_db_ApiBatchTask.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属项目下已有相同钩子ID,请重新生成!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ApiBatchTask.exists():
                    if basicInfo.taskId == obj_db_ApiBatchTask[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属项目下已有相同钩子ID,请重新生成!',
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
        cls_Logging.record_error_info('API', 'Api_BatchTask', 'data_save', errorMsg)
    else:
        obj_db_ApiBatchTask = db_ApiBatchTask.objects.filter(
            is_del=0, batchName=basicInfo.batchName, hookId=basicInfo.hookId)
        if obj_db_ApiBatchTask.exists():
            response['errorMsg'] = "当前项目下已有相同的批量任务名称或任务ID"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        None, None,
                        userId,
                        '【新增批量任务】', CUFront=responseData
                    )
                    # endregion
                    # region 保存基本信息
                    save_db_ApiBatchTask = db_ApiBatchTask.objects.create(
                        pid_id=basicInfo.proId, batchName=basicInfo.batchName, priority=basicInfo.priorityId,
                        remarks=basicInfo.remarks, pushTo=basicInfo.pushTo, hookState=basicInfo.hookState,
                        cuid=userId, uid_id=userId, is_del=0,
                    )
                    # endregion
                    # region 历史记录
                    # db_ApiTimingTaskHistory.objects.create(
                    #     timingTask_id=save_db_ApiTimingTask.id,
                    #     operationType='Add',
                    #     restoreData=responseData,
                    #     historyCode=historyCode,
                    #     uid_id=userId
                    # )
                    # endregion
                    # region 测试集
                    product_list_to_insert = list()
                    for item_index, item_testSet in enumerate(testSet, 0):
                        product_list_to_insert.append(db_ApiBatchTaskTestSet(
                            batchTask_id=save_db_ApiBatchTask.id,
                            index=item_index,
                            task_id=item_testSet.id,
                            state=1 if item_testSet.state else 0,
                            uid_id=userId,
                            is_del=0, )
                        )
                    db_ApiBatchTaskTestSet.objects.bulk_create(product_list_to_insert)
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['statusCode'] = 2001
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_batch_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        batchId = objData.batchId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_BatchTask', 'load_batch_data', errorMsg)
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
                'pushTo': ast.literal_eval(obj_db_ApiTimingTask[0].pushTo) if obj_db_ApiTimingTask[0].pushTo else [],
                'remarks': obj_db_ApiTimingTask[0].remarks,
            }
            # endregion
            # region 测试集
            testSet = []
            obj_db_ApiTimingTaskTestSet = db_ApiTimingTaskTestSet.objects.filter(
                is_del=0, timingTask_id=taskId).order_by('index')
            for item_testSet in obj_db_ApiTimingTaskTestSet:
                testSet.append({
                    'id': item_testSet.case_id,
                    'testType': item_testSet.case.testType,
                    'caseName': item_testSet.case.caseName,
                    'pageName': item_testSet.case.page.pageName,
                    'funName': item_testSet.case.fun.funName,
                    'caseState': item_testSet.case.caseState,
                    'state': True if item_testSet.state == 1 else False
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