from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from PageEnvironment.models import PageEnvironment as db_PageEnvironment
from Ui_CaseMaintenance.models import UiCaseBaseData as db_CaseBaseData
from Ui_CaseMaintenance.models import UiAssociatedPage as db_AssociatedPage

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.Redis import RedisHandle

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RedisHandle = RedisHandle()


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

        eventName = objData.eventName
        eventLogo = objData.eventLogo

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementEvent', 'select_data', errorMsg)
    else:
        # obj_db_ElementEvent = db_ElementEvent.objects.filter(is_del=0).order_by('index')
        # if eventName:
        #     obj_db_ElementEvent = obj_db_ElementEvent.filter(eventName__icontains=eventName)
        # if eventLogo:
        #     obj_db_ElementEvent = obj_db_ElementEvent.filter(eventLogo__icontains=eventLogo)
        # select_db_ElementEvent = obj_db_ElementEvent[minSize: maxSize]
        # for i in select_db_ElementEvent:
        #     obj_db_ElementEventComponent = db_ElementEventComponent.objects.filter(is_del=0, event_id=i.id)
        #     component = [{'id': item.id,
        #                   'label': item.label,
        #                   'state': True if item.state == 1 else False}
        #                  for item in obj_db_ElementEventComponent]
        #
        #     dataList.append({
        #         'id': i.id,
        #         'eventName': i.eventName,
        #         'eventLogo': i.eventLogo,
        #         'remarks': i.remarks,
        #         'component': component,
        #         "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
        #         "userName": f"{i.uid.userName}({i.uid.nickName})",
        #     })
        # response['TableData'] = dataList
        # response['Total'] = obj_db_ElementEvent.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 效验接用例数据的完成性
def charm_case_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        basicData = objData.BasicData
        testSet = objData.TestSet
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Ui_CaseMaintenance', 'charm_case_data', errorMsg)
    else:
        # region 验证基本信息
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(
            is_del=0, pid_id=basicData.proId, page_id=basicData.pageId, fun_id=basicData.funId,
            label=basicData.labelId, testType=basicData.testType, caseName=basicData.caseName
        )
        if obj_db_CaseBaseData.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属功能及同标签同类型下已有相同用例名称,请更改!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_CaseBaseData.exists():
                    if basicData.caseId == obj_db_CaseBaseData[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属功能及同标签同类型下已有相同用例名称,请更改!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证页面环境
        obj_db_PageEnvironment = db_PageEnvironment.objects.filter(is_del=0, id=basicData.environmentId)
        if not obj_db_PageEnvironment.exists():
            dataList.append({
                'stepsName': '基本信息',
                'errorMsg': '选择的页面环境不存在,请更改!',
                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证测试集
        for index_testSet, item_testSet in enumerate(testSet, 1):
            elementId = item_testSet.elementId
            if item_testSet.state:
                if item_testSet.elementType == ['InputEvent', 'Input']:
                    pass
                elif item_testSet.elementType in [['ClickEvent', 'Click'], ['DisplayEvent', 'Label']]:
                    if not elementId:
                        dataList.append({
                            'stepsName': f'测试集',
                            'errorMsg': f'第{index_testSet}行:选择元素不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                if item_testSet.assertType:
                    if not item_testSet.assertValueType:
                        dataList.append({
                            'stepsName': f'测试集',
                            'errorMsg': f'第{index_testSet}行:断言值类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                if item_testSet.assertValueType:
                    if not item_testSet.assertType:
                        dataList.append({
                            'stepsName': f'测试集',
                            'errorMsg': f'第{index_testSet}行:断言类型类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})

        # endregion
        response['statusCode'] = 2000
        response['TableData'] = dataList
    return JsonResponse(response)
