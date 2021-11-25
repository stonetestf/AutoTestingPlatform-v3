from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json

# Create your db here.
from info.models import OperateInfo as db_OperateInfo


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
def select_operational_info(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        sysType = objData.sysType

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', '2', 'info>select_operational_info', errorMsg)
    else:
        obj_db_OperateInfo = db_OperateInfo.objects.filter().order_by('-createTime')
        select_db_OperateInfo = obj_db_OperateInfo[minSize: maxSize]

        if sysType:
            obj_db_OperateInfo = obj_db_OperateInfo.filter(sysType=sysType)
            select_db_OperateInfo = obj_db_OperateInfo[minSize: maxSize]

        for i in select_db_OperateInfo:
            dataList.append({
                'id':i.id,
                'sysType':i.sysType,
                'toPage':i.toPage,
                'toFun':i.toFun,
                'CUFront':i.CUFront,
                'CURear':i.CURear,
                'userName':i.uid.userName,
                'createTime':str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_OperateInfo.count()
        response['statusCode'] = 2000
    return JsonResponse(response)