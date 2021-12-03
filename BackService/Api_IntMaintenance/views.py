from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json

# Create your db here.
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData

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
        sysType = objData.sysType
        proId = objData.proId
        environmentName = objData.environmentName
        environmentUrl = objData.environmentUrl

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageEnvironment', 'select_data', errorMsg)
    else:
        # obj_db_PageEnvironment = db_PageEnvironment.objects.filter(
        #     is_del=0, sysType=sysType, pid_id=proId).order_by('-updateTime')
        # select_db_PageEnvironment = obj_db_PageEnvironment[minSize: maxSize]
        # if environmentName:
        #     obj_db_PageEnvironment = obj_db_PageEnvironment.filter(environmentName__icontains=environmentName)
        #     select_db_PageEnvironment = obj_db_PageEnvironment[minSize: maxSize]
        # if environmentUrl:
        #     obj_db_PageEnvironment = obj_db_PageEnvironment.filter(environmentUrl__icontains=environmentUrl)
        #     select_db_PageEnvironment = obj_db_PageEnvironment[minSize: maxSize]
        # for i in select_db_PageEnvironment:
        #     dataList.append(
        #         {"id": i.id,
        #          "environmentName": i.environmentName,
        #          "environmentUrl": i.environmentUrl,
        #          "remarks": i.remarks,
        #          "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
        #          "userName": i.uid.userName,
        #          }
        #     )
        #
        # response['TableData'] = dataList
        # response['Total'] = obj_db_PageEnvironment.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 效验接口数据的完成性
def charm_api_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        basicInfo = objData.BasicInfo
        apiInfo = objData.ApiInfo
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'charm_api_data', errorMsg)
    else:
        # region 验证 接口名称,请求类型,请求地址
        if db_ApiBaseData.objects.filter(
                is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                apiName=basicInfo.apiName, requestType=apiInfo.requestType, requestUrl=apiInfo.requestUrl):
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属功能下已有相同接口数据,请更改!',
                    'updateTime': cls_Common.get_date_time()})
        else:
            if db_ApiBaseData.objects.filter(
                    is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                    apiName=basicInfo.apiName, requestType=apiInfo.requestType):
                if charmType:
                    dataList.append({
                        'stepsName': '基本信息',
                        'errorMsg': '当前所属功能下已有相同接口名称及请求类型,请更改!',
                        'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证请求URl
        if not apiInfo.requestUrl:
            dataList.append({
                'stepsName': '接口信息',
                'errorMsg': '不可新增接口请求地址为空的接口数据!',
                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 headers
        if apiInfo.request.headers:
            for index, item_headers in enumerate(apiInfo.request.headers, 1):
                if item_headers.state:
                    if not item_headers.key:
                        dataList.append({
                            'stepsName': '接口信息-Headers',
                            'errorMsg': f'第{index}行:参数名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 params
        if apiInfo.request.params:
            for index, item_params in enumerate(apiInfo.request.params, 1):
                if item_params.state:
                    if not item_params.key:
                        dataList.append({
                            'stepsName': '接口信息-Params',
                            'errorMsg': f'第{index}行:参数名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 body
        if apiInfo.request.body.requestSaveType == 'form-data':
            for index, item_body in enumerate(apiInfo.request.body.formData, 1):
                if item_body.state:
                    if not item_body.key:
                        dataList.append({
                            'stepsName': '接口信息-Body',
                            'errorMsg': f'第{index}行:参数名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 提取
        if apiInfo.request.extract:
            for index, item_extract in enumerate(apiInfo.request.extract, 1):
                if item_extract.state:
                    if not item_extract.key:
                        dataList.append({
                            'stepsName': '接口信息-Extract',
                            'errorMsg': f'第{index}行:变量名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_extract.value:
                        dataList.append({
                            'stepsName': '接口信息-Extract',
                            'errorMsg': f'第{index}行:提取表达式不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 断言
        if apiInfo.request.validate:
            for index, item_validate in enumerate(apiInfo.request.validate, 1):
                if item_validate.state:
                    if not item_validate.checkName:
                        dataList.append({
                            'stepsName': '接口信息-Validate',
                            'errorMsg': f'第{index}行:提取变量名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_validate.validateType:
                        dataList.append({
                            'stepsName': '接口信息-Validate',
                            'errorMsg': f'第{index}行:断言类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_validate.valueType:
                        dataList.append({
                            'stepsName': '接口信息-Validate',
                            'errorMsg': f'第{index}行:断言值类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 前置操作
        if apiInfo.request.preOperation:
            for index, item_preOperation in enumerate(apiInfo.request.preOperation, 1):
                if item_preOperation.state:
                    if item_preOperation.operationType == 'Methods':
                        if not item_preOperation.methodsName:
                            dataList.append({
                                'stepsName': '接口信息-前置操作',
                                'errorMsg': f'第{index}行:函数方法名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                    elif item_preOperation.operationType == 'DataBase':
                        if not item_preOperation.dataBase:
                            dataList.append({
                                'stepsName': '接口信息-前置操作',
                                'errorMsg': f'第{index}行:当前没有选择需要执行的数据库!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_preOperation.sql:
                            dataList.append({
                                'stepsName': '接口信息-前置操作',
                                'errorMsg': f'第{index}行:请输入SQL语句!',
                                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 后置操作
        if apiInfo.request.rearOperation:
            for index, item_rearOperation in enumerate(apiInfo.request.rearOperation, 1):
                if item_rearOperation.state:
                    if item_rearOperation.operationType == 'Methods':
                        if not item_rearOperation.methodsName:
                            dataList.append({
                                'stepsName': '接口信息-后置操作',
                                'errorMsg': f'第{index}行:函数方法名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                    elif item_rearOperation.operationType == 'DataBase':
                        if not item_rearOperation.dataBase:
                            dataList.append({
                                'stepsName': '接口信息-后置操作',
                                'errorMsg': f'第{index}行:当前没有选择需要执行的数据库!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_rearOperation.sql:
                            dataList.append({
                                'stepsName': '接口信息-后置操作',
                                'errorMsg': f'第{index}行:请输入SQL语句!',
                                'updateTime': cls_Common.get_date_time()})
        # endregion
        response['statusCode'] = 2000
        response['TableData'] = dataList
    return JsonResponse(response)

# @cls_Logging.log
# @cls_GlobalDer.foo_isToken
# @require_http_methods(["POST"])
# def save_data(request):
#     response = {}
#     try:
#         userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
#         sysType = request.POST['sysType']
#         proId = request.POST['proId']
#         environmentName = request.POST['environmentName']
#         environmentUrl = request.POST['environmentUrl']
#         remarks = request.POST['remarks']
#     except BaseException as e:
#         errorMsg = f"入参错误:{e}"
#         response['errorMsg'] = errorMsg
#         cls_Logging.record_error_info('API', 'PageEnvironment', 'data_save', errorMsg)
#     else:
#         obj_db_PageEnvironment = db_PageEnvironment.objects.filter(
#             is_del=0, sysType=sysType, pid_id=proId)
#         if obj_db_PageEnvironment.filter(environmentName=environmentName):
#             response['errorMsg'] = "当前所属项目下已有相同的环境名称存在,请更改!"
#         elif obj_db_PageEnvironment.filter(environmentUrl=environmentUrl):
#             response['errorMsg'] = "当前所属项目下已有相同的环境地址存在,请更改!"
#         else:
#             try:
#                 with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
#                     db_PageEnvironment.objects.create(
#                         sysType=sysType,
#                         pid_id=proId,
#                         environmentName=environmentName,
#                         environmentUrl=environmentUrl,
#                         remarks=remarks,
#                         is_del=0,
#                         uid_id=userId,
#                         cuid=userId
#                     )
#                     # region 添加操作信息
#                     cls_Logging.record_operation_info(
#                         'API', 'Manual', 3, 'Add',
#                         cls_FindTable.get_pro_name(proId), None, None,
#                         userId,
#                         '新增页面环境', CUFront=dict(request.POST)
#                     )
#                     # endregion
#             except BaseException as e:  # 自动回滚，不需要任何操作
#                 response['errorMsg'] = f'保存失败:{e}'
#             else:
#                 response['statusCode'] = 2001
#     return JsonResponse(response)
#
#
# @cls_Logging.log
# @cls_GlobalDer.foo_isToken
# @require_http_methods(["POST"])
# def edit_data(request):
#     response = {}
#     is_Edit = False
#     try:
#         userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
#         sysType = request.POST['sysType']
#         environmentId = int(request.POST['environmentId'])
#         proId = request.POST['proId']
#         environmentName = request.POST['environmentName']
#         environmentUrl = request.POST['environmentUrl']
#         remarks = request.POST['remarks']
#     except BaseException as e:
#         errorMsg = f"入参错误:{e}"
#         response['errorMsg'] = errorMsg
#         cls_Logging.record_error_info('API', 'PageEnvironment', 'edit_data', errorMsg)
#     else:
#         obj_db_PageEnvironment = db_PageEnvironment.objects.filter(id=environmentId, is_del=0)
#         if obj_db_PageEnvironment:
#             select_db_PageEnvironment = db_PageEnvironment.objects.filter(
#                 sysType=sysType, pid_id=proId, environmentName=environmentName, is_del=0)
#             if select_db_PageEnvironment:
#                 if environmentId == select_db_PageEnvironment[0].id:  # 自己修改自己
#                     is_Edit = True
#                 else:
#                     response['errorMsg'] = '当前项目下已有重复环境名称,请更改!'
#             else:
#                 is_Edit = True
#             if is_Edit:
#                 try:
#                     with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
#                         # region 添加操作信息
#                         oldData = list(obj_db_PageEnvironment.values())
#                         newData = dict(request.POST)
#                         cls_Logging.record_operation_info(
#                             'API', 'Manual', 3, 'Edit',
#                             cls_FindTable.get_pro_name(proId), None, None,
#                             userId,
#                             '修改页面环境',
#                             oldData, newData
#                         )
#                         # endregion
#                         obj_db_PageEnvironment.update(
#                             sysType=sysType,
#                             pid_id=proId,
#                             environmentName=environmentName,
#                             environmentUrl=environmentUrl,
#                             uid_id=userId,
#                             remarks=remarks,
#                             updateTime=cls_Common.get_date_time())
#                 except BaseException as e:  # 自动回滚，不需要任何操作
#                     response['errorMsg'] = f'数据修改失败:{e}'
#                 else:
#                     response['statusCode'] = 2002
#         else:
#             response['errorMsg'] = '未找当前页面环境,请刷新后重新尝试!'
#     return JsonResponse(response)
#
#
# @cls_Logging.log
# @cls_GlobalDer.foo_isToken
# @require_http_methods(["POST"])
# def delete_data(request):
#     response = {}
#     try:
#         userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
#         environmentId = request.POST['environmentId']
#     except BaseException as e:
#         errorMsg = f"入参错误:{e}"
#         response['errorMsg'] = errorMsg
#         cls_Logging.record_error_info('API', 'PageEnvironment', 'delete_data', errorMsg)
#     else:
#         obj_db_PageEnvironment = db_PageEnvironment.objects.filter(id=environmentId)
#         if obj_db_PageEnvironment:
#             try:
#                 with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
#                     obj_db_PageEnvironment.update(
#                         is_del=1,
#                         updateTime=cls_Common.get_date_time(),
#                         uid_id=userId,
#                     )
#                     # region 添加操作信息
#                     cls_Logging.record_operation_info(
#                         'API', 'Manual', 3, 'Delete',
#                         cls_FindTable.get_pro_name(obj_db_PageEnvironment[0].pid_id), None, None,
#                         userId,
#                         '删除页面环境', CUFront=dict(request.POST)
#                     )
#                     # endregion
#             except BaseException as e:  # 自动回滚，不需要任何操作
#                 response['errorMsg'] = f'数据删除失败:{e}'
#             else:
#                 response['statusCode'] = 2003
#         else:
#             response['errorMsg'] = '未找到当前页面环境,请刷新后重新尝试!'
#     return JsonResponse(response)
#
#
# @cls_Logging.log
# @cls_GlobalDer.foo_isToken
# @require_http_methods(["GET"])
# def get_page_environment_name_items(request):
#     response = {}
#     dataList = []
#     try:
#         responseData = json.loads(json.dumps(request.GET))
#         objData = cls_object_maker(responseData)
#         proId = objData.proId
#     except BaseException as e:
#         errorMsg = f"入参错误:{e}"
#         response['errorMsg'] = errorMsg
#         cls_Logging.record_error_info('API', 'PageEnvironment', 'get_page_environment_name_items', errorMsg)
#     else:
#         obj_db_PageEnvironment = db_PageEnvironment.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
#         for i in obj_db_PageEnvironment:
#             dataList.append({
#                 'label': i.environmentName, 'value': i.id
#             })
#         response['itemsData'] = dataList
#         response['statusCode'] = 2000
#     return JsonResponse(response)
