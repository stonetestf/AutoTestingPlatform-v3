from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from Api_TestReport.models import ApiTestReport as db_ApiTestReport
from Api_TestReport.models import ApiReportItem as db_ApiReportItem
from Api_TestReport.models import ApiQueue as db_ApiQueue


# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()


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
        reportName = objData.reportName
        reportType = objData.reportType
        queueStatus = objData.queueStatus

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TestReport', 'select_data', errorMsg)
    else:
        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        select_db_ApiTestReport = obj_db_ApiTestReport[minSize: maxSize]
        # if pageId:
        #     obj_db_FunManagement = obj_db_FunManagement.filter(page_id=pageId)
        #     select_db_FunManagement = obj_db_FunManagement[minSize: maxSize]
        # if funName:
        #     obj_db_FunManagement = obj_db_FunManagement.filter(funName__icontains=funName)
        #     select_db_FunManagement = obj_db_FunManagement[minSize: maxSize]
        for i in select_db_ApiTestReport:
            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0,testReport_id=i.id)
            obj_db_ApiQueue = db_ApiQueue.objects.filter(testReport_id=i.id)
            dataList.append(
                {"id": i.id,
                 "reportName": i.reportName,
                 "reportType": i.reportType,
                 "queueStatus": obj_db_ApiQueue[0].queueStatus if obj_db_ApiQueue.exists() else None,
                 "runningProgress": f"{obj_db_ApiReportItem.count()}/{i.apiTotal}",
                 "reportStatus": i.reportStatus if i.reportStatus else 'Error',
                 "runningTime":i.runningTime,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": i.uid.userName,
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_ApiTestReport.count()
        response['statusCode'] = 2000
    return JsonResponse(response)
