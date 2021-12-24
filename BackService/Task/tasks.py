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

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RequstOperation = RequstOperation()


@shared_task  # 异步任务-测试用例运行
def api_asynchronous_run_case(redisKey, caseId, environmentId, userId):
    # 组合成Case执行的用例
    cls_RequstOperation.run_case(redisKey,caseId,environmentId)


    return "int_asynchronous_run_case-测试用例运行完成"
