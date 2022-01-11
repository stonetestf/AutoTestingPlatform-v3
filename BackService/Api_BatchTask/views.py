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
from Api_BatchTask.models import ApiBatchTaskHistory as db_ApiBatchTaskHistory
from Api_CaseMaintenance.models import CaseTestSet as db_CaseTestSet

from Task.tasks import api_asynchronous_run_batch

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
                    if basicInfo.batchId == obj_db_ApiBatchTask[0].id:
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
                    if basicInfo.batchId == obj_db_ApiBatchTask[0].id:
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
        historyCode = cls_Common.generate_only_code()  # 生成历史记录唯一码
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
                        remarks=basicInfo.remarks, pushTo=basicInfo.pushTo,
                        hookState=basicInfo.hookState, hookId=basicInfo.hookId, historyCode=historyCode,
                        cuid=userId, uid_id=userId, is_del=0,
                    )
                    # endregion
                    # region 历史记录
                    db_ApiBatchTaskHistory.objects.create(
                        batchTask_id=save_db_ApiBatchTask.id,
                        operationType='Add',
                        restoreData=responseData,
                        historyCode=historyCode,
                        uid_id=userId
                    )
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
                            is_del=0,
                            historyCode=historyCode)
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
        obj_db_ApiBatchTask = db_ApiBatchTask.objects.filter(is_del=0, id=batchId)
        if obj_db_ApiBatchTask.exists():
            # region 基础信息
            basicInfo = {
                'batchName': obj_db_ApiBatchTask[0].batchName,
                'priorityId': obj_db_ApiBatchTask[0].priority,
                'pushTo': ast.literal_eval(obj_db_ApiBatchTask[0].pushTo) if obj_db_ApiBatchTask[0].pushTo else [],
                'remarks': obj_db_ApiBatchTask[0].remarks,
                'hookState': True if obj_db_ApiBatchTask[0].hookState == 1 else False,
                'hookId': obj_db_ApiBatchTask[0].hookId,
            }
            # endregion
            # region 测试集
            testSet = []
            obj_db_ApiBatchTaskTestSet = db_ApiBatchTaskTestSet.objects.filter(
                is_del=0, batchTask_id=batchId).order_by('index')
            for item_testSet in obj_db_ApiBatchTaskTestSet:
                # region 通过率
                obj_db_ApiTestReport = db_ApiTestReport.objects.filter(
                    is_del=0, reportType='TASK', taskId=item_testSet.task_id)
                passTotal = obj_db_ApiTestReport.filter(reportStatus='Pass').count()
                if obj_db_ApiTestReport.count() == 0:
                    passRate = 0
                else:
                    passRate = round(passTotal / obj_db_ApiTestReport.count() * 100, 2)
                # endregion
                testSet.append({
                    'id': item_testSet.task_id,
                    'taskName': item_testSet.task.taskName,
                    'caseTotal': db_ApiTimingTaskTestSet.objects.filter(is_del=0,
                                                                        timingTask_id=item_testSet.task_id).count(),
                    'taskState': True if item_testSet.task.taskStatus == 1 else False,
                    'passRate': f"{passRate}%",
                    'state': True if item_testSet.state == 1 else False,
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
        batchId = basicInfo.batchId
        historyCode = cls_Common.generate_only_code()  # 生成历史记录唯一码
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_BatchTask', 'edit_data', errorMsg)
    else:
        obj_db_ApiBatchTask = db_ApiBatchTask.objects.filter(is_del=0, id=batchId)
        if obj_db_ApiBatchTask.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    # region 查询以前的数据
                    oldTestSet = []
                    obj_db_ApiBatchTaskTestSet = db_ApiBatchTaskTestSet.objects.filter(
                        is_del=0, batchTask_id=batchId).order_by('index')
                    for item_testSet in obj_db_ApiBatchTaskTestSet:
                        oldTestSet.append({
                            'id': item_testSet.task_id,
                            'state': True if item_testSet.state == 1 else False,
                        })
                    oldData = {
                        'basicInfo': {
                            'batchName': obj_db_ApiBatchTask[0].batchName,
                            'priorityId': obj_db_ApiBatchTask[0].priority,
                            'pushTo': ast.literal_eval(obj_db_ApiBatchTask[0].pushTo) if obj_db_ApiBatchTask[
                                0].pushTo else [],
                            'remarks': obj_db_ApiBatchTask[0].remarks,
                            'hookState': True if obj_db_ApiBatchTask[0].hookState == 1 else False,
                            'hookId': obj_db_ApiBatchTask[0].hookId,
                        },
                        'testSet': oldTestSet,
                    }
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Edit',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        None, None,
                        userId,
                        f'【修改批量任务】 ID:{batchId}:{obj_db_ApiBatchTask[0].batchName}',
                        CUFront=oldData, CURear=responseData
                    )
                    # endregion
                    # endregion
                    # region 历史记录
                    db_ApiBatchTaskHistory.objects.create(
                        batchTask_id=batchId,
                        historyCode=historyCode,
                        operationType='Edit',
                        restoreData=oldData,
                        uid_id=userId
                    )
                    # endregion
                    # region 删除测试集数据
                    db_ApiBatchTaskTestSet.objects.filter(
                        is_del=0, batchTask_id=batchId, historyCode=obj_db_ApiBatchTask[0].historyCode).update(
                        is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId
                    )
                    # endregion
                    # region 更新基本信息
                    db_ApiBatchTask.objects.filter(is_del=0, id=batchId).update(
                        pid_id=basicInfo.proId, batchName=basicInfo.batchName, priority=basicInfo.priorityId,
                        remarks=basicInfo.remarks, pushTo=basicInfo.pushTo, historyCode=historyCode,
                        hookState=basicInfo.hookState, hookId=basicInfo.hookId, uid_id=userId, is_del=0,
                    )
                    # endregion
                    # region 新增测试集数据
                    product_list_to_insert = list()
                    for item_index, item_testSet in enumerate(testSet, 0):
                        product_list_to_insert.append(db_ApiBatchTaskTestSet(
                            batchTask_id=batchId,
                            index=item_index,
                            task_id=item_testSet.id,
                            state=1 if item_testSet.state else 0,
                            uid_id=userId,
                            is_del=0,
                            historyCode=historyCode)
                        )
                    db_ApiBatchTaskTestSet.objects.bulk_create(product_list_to_insert)
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找到当前批量任务,请刷新后在重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        batchId = request.POST['batchId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_BatchTask', 'delete_data', errorMsg)
    else:
        obj_db_ApiBatchTask = db_ApiBatchTask.objects.filter(id=batchId, is_del=0)
        if obj_db_ApiBatchTask.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加历史恢复
                    db_ApiBatchTaskHistory.objects.create(
                        batchTask_id=batchId,
                        operationType='Delete',
                        restoreData=None,
                        uid_id=userId,
                        historyCode=None,
                    )
                    # endregion
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Delete',
                        cls_FindTable.get_pro_name(obj_db_ApiBatchTask[0].pid_id),
                        None, None,
                        userId,
                        f'【删除批量任务】 ID:{batchId}:{obj_db_ApiBatchTask[0].batchName}',
                        CUFront=json.dumps(request.POST)
                    )
                    # endregion
                    # region 删除关联信息
                    db_ApiBatchTaskTestSet.objects.filter(
                        is_del=0, batchTask_id=batchId, historyCode=obj_db_ApiBatchTask[0].historyCode).update(
                        is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId
                    )
                    obj_db_ApiBatchTask.update(
                        is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'数据删除失败:{e}'
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前批量任务,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 运行
def execute_batch_task(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        batchId = request.POST['batchId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_BatchTask', 'execute_batch_task', errorMsg)
    else:
        obj_db_ApiBatchTask = db_ApiBatchTask.objects.filter(is_del=0, id=batchId)
        if obj_db_ApiBatchTask.exists():
            queueState = cls_FindTable.get_queue_state('BATCH', batchId)
            if queueState:
                response['errorMsg'] = '当前已有相同批量任务在运行,不可重复运行!您可在主页中项目里查看此用例的动态!' \
                                       '如遇错误可取消该项目队列后重新运行!'
            else:
                # region 获取当前批量任务的需要运行多少个接口
                total = 0
                obj_db_ApiBatchTaskTestSet = db_ApiBatchTaskTestSet.objects.filter(is_del=0, batchTask_id=batchId)
                for item_taskSet in obj_db_ApiBatchTaskTestSet:
                    if item_taskSet.state == 1:
                        obj_db_ApiTimingTaskTestSet = db_ApiTimingTaskTestSet.objects.filter(
                            is_del=0, timingTask_id=item_taskSet.task_id)
                        for item_caseSet in obj_db_ApiTimingTaskTestSet:
                            if item_caseSet.state == 1:
                                total += db_CaseTestSet.objects.filter(
                                    is_del=0, caseId_id=item_caseSet.case_id,state=1).count()
                # endregion
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 创建1级主报告
                        # 批量任务的报告是不同的有4层! 接口,用例,定时任务只有3层,
                        # 1级主报告>定时任务报告>用例报告>接口报告
                        createTestReport = cls_ApiReport.create_test_report(
                            obj_db_ApiBatchTask[0].pid_id,
                            obj_db_ApiBatchTask[0].batchName,
                            'BATCH', batchId, total, userId
                        )
                        # endregion
                        if createTestReport['state']:
                            testReportId = createTestReport['testReportId']
                            # region 创建队列
                            queueId = cls_ApiReport.create_queue(
                                obj_db_ApiBatchTask[0].pid_id, None, None,
                                'BATCH', batchId, testReportId, userId)  # 创建队列
                            # endregion
                        else:
                            raise ValueError(f'创建主测试报告失败:{createTestReport["errorMsg"]}')
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f"失败:{e}"
                else:
                    # environmentId = obj_db_ApiTimingTask[0].environment_id
                    # taskName = obj_db_ApiTimingTask[0].taskName
                    remindLabel = f"批量任务:{obj_db_ApiBatchTask[0].batchName}>"  # 推送的标识
                    result = api_asynchronous_run_batch.delay(testReportId, queueId, batchId,remindLabel,userId)
                    if result.task_id:
                        response['statusCode'] = 2001
                        response['celeryTaskId'] = result.task_id
        else:
            response['errorMsg'] = '当前选择的批量任务不存在,请刷新后在重新尝试!'
    return JsonResponse(response)
