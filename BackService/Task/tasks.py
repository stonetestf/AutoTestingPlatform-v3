from celery import shared_task

import json
import ast

# Create your db here.


# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
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


@shared_task  # 异步任务-测试用例运行
def api_asynchronous_run_case(redisKey, testReportId, queueId, caseId, environmentId, userId):
    cls_ApiReport.update_queue(queueId, 1, userId)  # 更新队列-执行中
    # 组合成Case执行的用例
    cls_RequstOperation.execute_case(redisKey, testReportId, caseId, environmentId, userId)
    cls_ApiReport.get_report_top_data(testReportId)  # 更新主测试报告
    cls_ApiReport.update_queue(queueId, 2, userId)  # 更新队列-完成

    return "int_asynchronous_run_case-测试用例运行完成"
