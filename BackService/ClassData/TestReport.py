# Create your db here.
from Api_TestReport.models import ApiTestReport as db_ApiTestReport
from Api_TestReport.models import ApiReportItem as db_ApiReportItem
from Api_TestReport.models import ApiReport as db_ApiReport
from Api_TestReport.models import ApiQueue as db_ApiQueue

import ast
import json

# Create reference here.
from ClassData.Logger import Logging as cls_Logging
from ClassData.Common import Common

cls_Common = Common()


class ApiReport(cls_Logging):
    # 创建主1级报告
    def create_test_report(self, proId, reportName, reportType, taskId, apiTotal, userId):
        """
        :param proId:
        :param reportName:
        :param reportType: 报告类型(API:单接口,CASE:测试用例,TASK:定时任务,BATCH:批量任务)
        :param taskId: ApiId/CaseId/TaskId/BatchId,根据任务类型来取
        :param apiTotal:
        :param userId:
        :return:
        """
        results = {}
        try:
            save_db_ApiTestReport = db_ApiTestReport.objects.create(
                pid_id=proId,
                reportName=reportName,
                reportType=reportType,
                taskId=taskId,
                apiTotal=apiTotal,
                uid_id=userId,
                is_del=0,
            )
        except BaseException as e:
            results['state'] = False
            errorMsg = f"保存失败:{e}"
            results['errorMsg'] = errorMsg
            cls_Logging.record_error_info(self, 'API', 'ClassData>TestReport>ApiReport', 'create_test_report', errorMsg)
        else:
            results['state'] = True
            results['testReportId'] = save_db_ApiTestReport.id
        return results

    # 创建2级报告列表
    def create_report_items(self, testReportId, apiId, apiName, ctbId=None):
        """
        :param testReportId:
        :param apiId:
        :param apiName:
        :param ctbId: 单接口没有此ID/Case,Task,Batch类型时这里显示CaseId
        :return:
        """
        results = {}
        try:
            save_db_ApiReportItem = db_ApiReportItem.objects.create(
                testReport_id=testReportId,
                apiId_id=apiId,
                apiName=apiName,
                ctbId=ctbId,
                successTotal=0,
                failTotal=0,
                errorTotal=0,
                is_del=0,
            )
        except BaseException as e:
            results['state'] = False
            errorMsg = f"保存失败:{e}"
            results['errorMsg'] = errorMsg
            cls_Logging.record_error_info(
                self, 'API', 'ClassData>TestReport>ApiReport', 'create_report_items', errorMsg)
        else:
            results['state'] = True
            results['reportItemId'] = save_db_ApiReportItem.id
        return results

    # 创建单接口报告
    def create_api_report(self, reportItemId, results):
        try:
            db_ApiReport.objects.create(
                reportItem_id=reportItemId,
                requestUrl=results['request']['requestUrl'],
                requestType=results['request']['requestType'],
                requestHeaders=results['request']['headersDict'],
                requestData=results['request']['requestDataDict'],
                # requestFile=results['requestFile'],
                reportStatus=results['response']['reportState'],

                statusCode=results['response']['responseCode'],
                responseHeaders=results['response']['responseHeaders'],
                responseInfo=results['response']['text'],
                requestExtract=results['response']['extractTable'],

                # responseExtract=results['response']['responseExtract'],
                responseValidate=results['response']['assertionTable'],

                preOperationInfo=results['response']['preOperationTable'],
                rearOperationInfo=results['response']['rearOperationTable'],
                errorInfo=results['response']['errorInfoTable'],
                runningTime=results['response']['time'],
                is_del=0,
            )
        except BaseException as e:
            errorMsg = f"保存失败:{e}"
            cls_Logging.print_log(self, 'error', 'create_api_report', errorMsg)
            cls_Logging.record_error_info(self, 'API', 'ClassData>TestReport>ApiReport', 'create_api_report', errorMsg)

    # 更新 成功失败数量及运行总时间
    def update_report_items(self, testReportId, reportItemId):
        successTotal = 0
        failTotal = 0
        errorTotal = 0
        itemRunningTime = 0  # db_ApiReportItem的统计耗时
        testReportRunningTime = 0  # db_ApiTestReport的统计耗时
        reportStatus = None
        obj_db_ApiReport = db_ApiReport.objects.filter(is_del=0, reportItem_id=reportItemId)
        for i in obj_db_ApiReport:
            if i.reportStatus == 'Pass':
                successTotal += 1
            elif i.reportStatus == 'Fail':
                failTotal += 1
            else:  # Error
                errorTotal += 1

            itemRunningTime += float(i.runningTime)

        # 更新报告成功失败数
        db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId, id=reportItemId).update(
            successTotal=successTotal, failTotal=failTotal, errorTotal=errorTotal, runningTime=itemRunningTime,
            updateTime=cls_Common.get_date_time()
        )

        if failTotal + errorTotal >= 1:
            if failTotal >= 1:
                reportStatus = 'Fail'
            if errorTotal >= 1:
                reportStatus = 'Error'
        else:
            reportStatus = 'Pass'
        db_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId)
        for i in db_db_ApiReportItem:
            testReportRunningTime += float(i.runningTime)
        db_ApiTestReport.objects.filter(id=testReportId).update(
            reportStatus=reportStatus, runningTime=testReportRunningTime, updateTime=cls_Common.get_date_time()
        )

    # 创建队列
    def create_queue(self, proId, pageId, funId, taskType, taskId, testReportId, userId):
        """
        :param taskId: 务ID,apiId,CaseId,TaskId,BatchId
        :param testReportId:
        :param userId:
        :return:
        """
        save_db_ApiQueue = db_ApiQueue.objects.create(
            pid_id=proId, page_id=pageId, fun_id=funId, taskType=taskType, taskId=taskId, testReport_id=testReportId,
            queueStatus=0, uid_id=userId
        )
        return save_db_ApiQueue.id

    # 更新队列状态
    def update_queue(self, queueId, queueStatus, userId):
        """
        :param taskId: 务ID,apiId,CaseId,TaskId,BatchId
        :param testReportId:
        :param queueStatus: 队列执行状态(0:未开始,1:执行中,2:已结束)
        :param userId:
        :return:
        """
        db_ApiQueue.objects.filter(id=queueId).update(queueStatus=queueStatus, uid_id=userId)

    # 测试报告-返回顶部数据
    def get_report_top_data(self, testReportId):
        results = {
            'errorMsg': '',
            'topData': {
                'reportName': None,
                'createTime': '',
                'runningTime': 0,
                'reportStatus': None,
                'passTotal': 0,
                'failTotal': 0,
                'errorTotal': 0,
                'passRate': 0,  # 通过率
                'failedTotal': 0,  # 未执行'
            }
        }

        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(id=testReportId, is_del=0)
        if obj_db_ApiTestReport.exists():
            reportName = obj_db_ApiTestReport[0].reportName
            createTime = str(obj_db_ApiTestReport[0].updateTime.strftime('%Y-%m-%d %H:%M:%S'))
            reportStatus = obj_db_ApiTestReport[0].reportStatus
            apiTotal = obj_db_ApiTestReport[0].apiTotal
            results['topData']['reportName'] = reportName
            results['topData']['createTime'] = createTime
            results['topData']['reportStatus'] = reportStatus

            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId)
            passTotal = 0
            failTotal = 0
            errorTotal = 0
            runningTime = 0
            failedTotal = apiTotal  # 未执行数

            prePassTotal = 0  # 前置成功
            rearPassTotal = 0  # 后置成功
            extractPassTotal = 0  # 提取成功
            assertionsPassTotal = 0  # 断言成功
            for item_reportItem in obj_db_ApiReportItem:
                passTotal += float(item_reportItem.successTotal)
                failTotal += float(item_reportItem.failTotal)
                errorTotal += float(item_reportItem.errorTotal)
                failedTotal -= 1

                obj_db_ApiReport = db_ApiReport.objects.filter(is_del=0, reportItem_id=item_reportItem.id)
                for item_apiReport in obj_db_ApiReport:
                    runningTime += float(item_apiReport.runningTime)
                    # region 前置数
                    if item_apiReport.preOperationInfo:
                        preOperationInfo = ast.literal_eval(item_apiReport.preOperationInfo)
                    else:
                        preOperationInfo = []
                    for item_pre in preOperationInfo:
                        if item_pre['resultsState']:
                            prePassTotal += 1
                    # endregion
                    # region 后置数
                    if item_apiReport.rearOperationInfo:
                        rearOperationInfo = ast.literal_eval(item_apiReport.rearOperationInfo)
                    else:
                        rearOperationInfo = []
                    for item_rear in rearOperationInfo:
                        if item_rear['resultsState']:
                            rearPassTotal += 1
                    # endregion
                    # region 提取数
                    if item_apiReport.requestExtract:
                        requestExtract = ast.literal_eval(item_apiReport.requestExtract)
                        extractPassTotal += len(requestExtract)

                    # endregion
                    # region 断言数
                    if item_apiReport.responseValidate:
                        responseValidate = ast.literal_eval(item_apiReport.responseValidate)
                    else:
                        responseValidate = []
                    for item_validate in responseValidate:
                        if item_validate['results']:
                            assertionsPassTotal += 1
                    # endregion
            results['topData']['passTotal'] = passTotal
            results['topData']['failTotal'] = failTotal
            results['topData']['errorTotal'] = errorTotal
            results['topData']['runningTime'] = round(runningTime, 2)
            results['topData']['failedTotal'] = failedTotal

            allTotal = passTotal + failTotal + errorTotal
            passRate = passTotal / allTotal * 100
            results['topData']['passRate'] = int(passRate)

            results['topData']['prePassTotal'] = prePassTotal
            results['topData']['rearPassTotal'] = rearPassTotal
            results['topData']['assertionsPassTotal'] = assertionsPassTotal
            results['topData']['extractPassTotal'] = extractPassTotal
            results['state'] = True
        else:
            results['state'] = False
            results['errorMsg'] = "当前选择测试报告不存在,请刷新后在重新尝试!"
        return results

    # 测试报告-返回一级列表数据
    def get_report_first_list(self, testReportId):
        # 根据报告的类型 展示第1层列表是 接口 用例 定时任务 批量任务
        results = {}
        firstList = []
        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(id=testReportId)
        if obj_db_ApiTestReport.exists():
            reportType = obj_db_ApiTestReport[0].reportType
            if reportType == "API" or reportType == "CASE":
                obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId)
                for i in obj_db_ApiReportItem:
                    passTotal = i.successTotal
                    failTotal = i.failTotal
                    errorTotal = i.errorTotal
                    if passTotal + failTotal + errorTotal == 0:
                        reportStatus = 'Error'
                    elif errorTotal >= 1:
                        reportStatus = 'Error'
                    elif failTotal >= 1:
                        reportStatus = 'Fail'
                    else:
                        reportStatus = 'Pass'

                    firstList.append({
                        'id': i.id,
                        'name': i.apiName,
                        'reportStatus': reportStatus,
                    })

                results['state'] = True
                results['firstList'] = firstList
            else:
                pass
        else:
            results['state'] = False
            results['errorMsg'] = "当前选择的报告数据缺失!"
        return results

    def get_report_api(self, reportItemId):
        results = {}
        obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, id=reportItemId)
        if obj_db_ApiReportItem.exists():
            obj_db_ApiReport = db_ApiReport.objects.filter(is_del=0, reportItem_id=obj_db_ApiReportItem[0].id)
            if obj_db_ApiReport.exists():
                general = []  # 基本信息
                requestHeaders = []
                requestData = []
                operationData = []  # 包含前置和后置
                # region 保存基本信息
                general.append({'key': 'Request URL:', 'value': obj_db_ApiReport[0].requestUrl})
                general.append({'key': 'Request Type:', 'value': obj_db_ApiReport[0].requestType})
                general.append({'key': 'Status Code:', 'value': obj_db_ApiReport[0].statusCode})
                # endregion
                # region 保存请求头
                ret_requestHeaders = ast.literal_eval(obj_db_ApiReport[0].requestHeaders)
                for item_header in ret_requestHeaders:
                    requestHeaders.append({'key': item_header, 'value': ret_requestHeaders[item_header]})
                # endregion
                # region 反回求头
                if obj_db_ApiReport[0].responseHeaders:
                    responseHeaders = ast.literal_eval(obj_db_ApiReport[0].responseHeaders)
                else:
                    responseHeaders = []
                # endregion
                # region 保存请求主体
                ret_requestData = ast.literal_eval(obj_db_ApiReport[0].requestData)
                for item_body in ret_requestData:
                    requestData.append({'key': item_body, 'value': ret_requestData[item_body]})
                # endregion
                # region 返回主体信息
                try:
                    ret_responseInfo = eval(obj_db_ApiReport[0].responseInfo)
                    responseInfo = json.dumps(ret_responseInfo, indent=4, separators=(',', ':'), ensure_ascii=False)
                except BaseException as e:
                    responseInfo = obj_db_ApiReport[0].responseInfo
                # endregion
                # region  提取
                if obj_db_ApiReport[0].requestExtract:
                    extract = ast.literal_eval(obj_db_ApiReport[0].requestExtract)
                else:
                    extract = []
                # endregion
                # region 断言
                if obj_db_ApiReport[0].responseValidate:
                    validateResults = ast.literal_eval(obj_db_ApiReport[0].responseValidate)  # 断言结果
                else:
                    validateResults = []
                # endregion
                # region 前后置操作
                if obj_db_ApiReport[0].preOperationInfo:
                    preOperationInfo = ast.literal_eval(obj_db_ApiReport[0].preOperationInfo)
                else:
                    preOperationInfo = []

                if obj_db_ApiReport[0].rearOperationInfo:
                    rearOperationInfo = ast.literal_eval(obj_db_ApiReport[0].rearOperationInfo)
                else:
                    rearOperationInfo = []

                for item_pre in preOperationInfo:
                    operationData.append({
                        'operatingPosition': 'Pre',
                        'operationType': item_pre['operationType'],
                        'callName': item_pre['callName'],
                        'callResults': item_pre['callResults'],
                        'resultsState': item_pre['resultsState']
                    })
                for item_rear in rearOperationInfo:
                    operationData.append({
                        'operatingPosition': 'Rear',
                        'operationType': item_rear['operationType'],
                        'callName': item_rear['callName'],
                        'callResults': item_rear['callResults'],
                        'resultsState': item_rear['resultsState']
                    })
                # endregion
                # region 错误信息
                if obj_db_ApiReport[0].errorInfo:
                    errorTableData = ast.literal_eval(obj_db_ApiReport[0].errorInfo)
                else:
                    errorTableData = []
                # endregion
                dataDict = {
                    'general': general,
                    'requestHeaders': requestHeaders,
                    'requestData': requestData,
                    'responseHeaders': responseHeaders,
                    'responseInfo': responseInfo,
                    'extract': extract,
                    'validateResults': validateResults,
                    'operationData': operationData,
                    'errorTableData': errorTableData,
                }
                results['state'] = True
                results['dataDict'] = dataDict
        else:
            results['state'] = False
            results['errorMsg'] = '未找到当前选择的接口数据!'

        return results


class UiReport(cls_Logging):
    pass


class PtsReport(cls_Logging):
    pass
