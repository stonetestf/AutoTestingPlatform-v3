from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q

import json
import ast

# Create your db here.
from Api_CaseMaintenance.models import CaseBaseData as db_CaseBaseData

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
            obj_db_CaseBaseData = db_CaseBaseData.objects.filter(~Q(id__in=passCaseIdList),is_del=0,pid_id=proId)
        else:
            obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0,pid_id=proId)
        if pageId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(page_id=pageId)
        if funId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(fun_id=funId)

        for i in obj_db_CaseBaseData:
            dataList.append({
                'id':i.id,
                'pageName':i.page.pageName,
                'funName':i.fun.funName,
                'caseName':i.caseName,
                'caseState':i.caseState,
                'testType':i.testType,
                "userName": f"{i.uid.userName}({i.uid.nickName})",
            })

        response['TableData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)
