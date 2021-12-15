# Create your db here.
from Api_TestReport.models import ApiTestReport as db_ApiTestReport
from Api_TestReport.models import ApiReportItem as db_ApiReportItem
from Api_TestReport.models import ApiReport as db_ApiReport
from Api_TestReport.models import ApiQueue as db_ApiQueue

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
                requestUrl=results['requestUrl'],
                requestType=results['requestType'],
                requestHeaders=results['report']['requsetHeaders'],
                requestData=results['report']['requestData'],
                # requestFile=results['requestFile'],
                reportStatus=results['reportState'],

                statusCode=results['responseCode'],
                # responseHeaders=results['report']['responseHeaders'],
                responseInfo=results['tabPane']['text'],
                # requestExtract=results['requestExtract'],
                # requestValidate=results['requestValidate'],
                # responseValidate=results['responseValidate'],
                # responseMethods=results['responseMethods'],
                errorInfo=results['errorInfo'],
                runningTime=results['time'],
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
            match i.reportStatus:
                case 'Pass':
                    successTotal += 1
                case 'Fail':
                    failTotal += 1
                case 'Error':
                    errorTotal += 1
            itemRunningTime += float(i.runningTime)

        db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId).update(
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
            }
        }

        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(id=testReportId, is_del=0)
        if obj_db_ApiTestReport.exists():
            reportName = obj_db_ApiTestReport[0].reportName
            createTime = str(obj_db_ApiTestReport[0].updateTime.strftime('%Y-%m-%d %H:%M:%S'))
            reportStatus = obj_db_ApiTestReport[0].reportStatus
            results['topData']['reportName'] = reportName
            results['topData']['createTime'] = createTime
            results['topData']['reportStatus'] = reportStatus

            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId)
            passTotal = 0
            failTotal = 0
            errorTotal = 0
            runningTime = 0
            for item_reportItem in obj_db_ApiReportItem:
                passTotal += float(item_reportItem.successTotal)
                failTotal += float(item_reportItem.failTotal)
                errorTotal += float(item_reportItem.errorTotal)

                obj_db_ApiReport = db_ApiReport.objects.filter(is_del=0, reportItem_id=item_reportItem.id)
                for item_apiReport in obj_db_ApiReport:
                    runningTime += float(item_apiReport.runningTime)
            results['topData']['passTotal'] = passTotal
            results['topData']['failTotal'] = failTotal
            results['topData']['errorTotal'] = errorTotal
            results['topData']['runningTime'] = runningTime

            allTotal = passTotal + failTotal + errorTotal
            passRate = passTotal / allTotal * 100
            results['topData']['passRate'] = int(passRate)
            results['state'] = True
        else:
            results['state'] = False
            results['errorMsg'] = "当前选择测试报告不存在,请刷新后在重新尝试!"
        return results

    # 测试报告-返回一级列表数据
    def get_report_first_list(self,testReportId):
        results={}


class UiReport(cls_Logging):
    pass


class PtsReport(cls_Logging):
    pass
