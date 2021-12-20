from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from ProjectManagement.models import ProManagement as db_ProManagement
from PageManagement.models import PageManagement as db_PageManagement
from FunManagement.models import FunManagement as db_FunManagement
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData
from Api_IntMaintenance.models import ApiHeaders as db_ApiHeaders
from Api_IntMaintenance.models import ApiParams as db_ApiParams
from Api_IntMaintenance.models import ApiBody as db_ApiBody
from Api_IntMaintenance.models import ApiExtract as db_ApiExtract
from Api_IntMaintenance.models import ApiValidate as db_ApiValidate
from Api_IntMaintenance.models import ApiOperation as db_ApiOperation

from Api_CaseMaintenance.models import CaseBaseData as dbCaseBaseData



from Api_IntMaintenance.models import ApiAssociatedUser as db_ApiAssociatedUser
from WorkorderManagement.models import WorkorderManagement as db_WorkorderManagement
from WorkorderManagement.models import WorkBindPushToUsers as db_WorkBindPushToUsers
from WorkorderManagement.models import WorkLifeCycle as db_WorkLifeCycle
from Api_IntMaintenance.models import ApiHistory as db_ApiHistory
from PageEnvironment.models import PageEnvironment as db_PageEnvironment

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
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


# Create your views here.

@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_data(request):
    response = {}
    headers = []
    params = []
    body = []
    extract = []
    validate = []
    preOperation = []  # 前置操作
    rearOperation = []  # 后置操作
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        apiId = objData.apiId
        synchronous = True if objData.synchronous == 'true' else False
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'load_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, id=apiId)
        if obj_db_ApiBaseData.exists():
            if synchronous:  # 是否开启了接口同步功能，开启时取API维护的请求数据,没开启时取CaseApi的独立数据
                requestType = obj_db_ApiBaseData[0].requestType
                requestUrlRadio = obj_db_ApiBaseData[0].requestUrlRadio
                requestUrl = ast.literal_eval(obj_db_ApiBaseData[0].requestUrl)[f'url{requestUrlRadio}']
                # region headers
                obj_db_ApiHeaders = db_ApiHeaders.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
                for item_headers in obj_db_ApiHeaders:
                    headers.append({
                        'index': item_headers.index,
                        'key': item_headers.key,
                        'value': item_headers.value,
                        'remarks': item_headers.remarks,
                        'state': True if item_headers.state else False,
                    })
                # endregion
                # region params
                obj_db_ApiParams = db_ApiParams.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
                for item_params in obj_db_ApiParams:
                    params.append({
                        'index': item_params.index,
                        'key': item_params.key,
                        'value': item_params.value,
                        'remarks': item_params.remarks,
                        'state': True if item_params.state else False,
                    })
                # endregion
                # region body
                bodyData = None
                obj_db_ApiBody = db_ApiBody.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
                requestSaveType = obj_db_ApiBaseData[0].bodyRequestSaveType
                if obj_db_ApiBaseData[0].bodyRequestSaveType == 'form-data':
                    for item_body in obj_db_ApiBody:
                        body.append({
                            'index': item_body.index,
                            'key': item_body.key,
                            'value': item_body.value,
                            'remarks': item_body.remarks,
                            'state': True if item_body.state else False,
                        })
                    bodyData = body
                elif obj_db_ApiBaseData[0].bodyRequestSaveType == 'raw':
                    bodyData = obj_db_ApiBody[0].value
                # endregion
            else:

                requestType = None
                requestUrl = None
                headers = []
                params = []
                requestSaveType = None
                bodyData = None

            # region extract
            obj_db_ApiExtract = db_ApiExtract.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            for item_extract in obj_db_ApiExtract:
                extract.append({
                    'index': item_extract.index,
                    'key': item_extract.key,
                    'value': item_extract.value,
                    'remarks': item_extract.remarks,
                    'state': True if item_extract.state else False,
                })
            # endregion
            # region validate
            obj_db_ApiValidate = db_ApiValidate.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            for item_validate in obj_db_ApiValidate:
                validate.append({
                    'index': item_validate.index,
                    'checkName': item_validate.checkName,
                    'validateType': item_validate.validateType,
                    'valueType': item_validate.valueType,
                    'expectedResults': item_validate.expectedResults,
                    'remarks': item_validate.remarks,
                    'state': True if item_validate.state else False,
                })
            # endregion
            # region 前置操作
            obj_db_ApiOperation = db_ApiOperation.objects.filter(
                is_del=0, apiId_id=apiId, location='Pre').order_by('index')
            for item_preOperation in obj_db_ApiOperation:
                preOperation.append({
                    'index': item_preOperation.index,
                    'operationType': item_preOperation.operationType,
                    'methodsName': item_preOperation.methodsName,
                    'dataBase': item_preOperation.dataBaseId,
                    'sql': item_preOperation.sql,
                    'remarks': item_preOperation.remarks,
                    'state': True if item_preOperation.state else False,
                })
            # endregion
            # region 后置操作
            obj_db_ApiOperation = db_ApiOperation.objects.filter(
                is_del=0, apiId_id=apiId, location='Rear').order_by('index')
            for item_rearOperation in obj_db_ApiOperation:
                rearOperation.append({
                    'index': item_rearOperation.index,
                    'operationType': item_rearOperation.operationType,
                    'methodsName': item_rearOperation.methodsName,
                    'dataBase': item_rearOperation.dataBaseId,
                    'sql': item_rearOperation.sql,
                    'remarks': item_rearOperation.remarks,
                    'state': True if item_rearOperation.state else False,
                })
            # endregion
            apiInfo = {
                'requestType':requestType,
                'requestUrl': requestUrl,
                'request': {
                    'headers': headers,
                    'params': params,
                    'body': {
                        'requestSaveType': requestSaveType,
                        'bodyData': bodyData
                    },
                    'extract': extract,
                    'validate': validate,
                    'preOperation': preOperation,
                    'rearOperation': rearOperation,
                }
            }

            response['apiInfo'] = apiInfo
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = "未找到当前选择的接口数据,请刷新后重新尝试!"
    return JsonResponse(response)
