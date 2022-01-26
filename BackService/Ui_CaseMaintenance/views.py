from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from PageEnvironment.models import PageEnvironment as db_PageEnvironment
from Ui_CaseMaintenance.models import UiCaseBaseData as db_CaseBaseData
from Ui_CaseMaintenance.models import UiAssociatedPage as db_AssociatedPage
from Ui_CaseMaintenance.models import UiTestSet as db_TestSet
from Ui_ElementEvent.models import ElementEventComponent as db_ElementEventComponent

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

        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        proId = objData.proId
        pageId = objData.pageId
        funId = objData.funId
        labelId = objData.labelId
        caseState = objData.caseState
        caseName = objData.caseName
        associations = objData.associations

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_CaseMaintenance', 'select_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        if pageId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(page_id=pageId)
        if funId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(fun_id=funId)
        # if testType:
        #     obj_db_CaseBaseData = obj_db_CaseBaseData.filter(testType=testType)
        if labelId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(label=labelId)
        if caseState:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(caseState=caseState)
        if caseName:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(caseName__icontains=caseName)
        select_db_CaseBaseData = obj_db_CaseBaseData[minSize: maxSize]
        for i in select_db_CaseBaseData:
            tableItem = []
            obj_db_TestSet = db_TestSet.objects.filter(is_del=0, case_id=i.id)
            for item_testSet in obj_db_TestSet:

                elementType = ast.literal_eval(item_testSet.elementType)
                obj_db_ElementEventComponent = db_ElementEventComponent.objects.filter(is_del=0,value=elementType[1])
                if obj_db_ElementEventComponent.exists():
                    elementTypeTxt = obj_db_ElementEventComponent[0].label
                else:
                    elementTypeTxt = ""
                tableItem.append({
                    'index': item_testSet.index,
                    'eventName': item_testSet.eventName,
                    'elementTypeTxt': elementTypeTxt,
                    'inputData': item_testSet.inputData,
                    # 'requestParamsType': requestParamsType,
                    'state': True if item_testSet.state == 1 else False,
                    'updateTime': str(item_testSet.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                })
            if associations == 'My':
                # 当前查询的用户是修改者 或是 创建者
                if userId == i.uid_id or userId == i.cuid:
                    dataList.append({
                        'id': i.id,
                        'tableItem': tableItem,
                        'priority': i.priority,
                        'testType': i.testType,
                        'caseName': i.caseName,
                        'pageName': i.page.pageName,
                        'funName': i.fun.funName,
                        'labelId': i.label,
                        'elementdynamic': False,
                        'caseState': i.caseState,
                        'passRate': 0,
                        'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                        "userName": f"{i.uid.userName}({i.uid.nickName})",
                        'createUserName': cls_FindTable.get_userName(i.cuid),
                    })
            else:
                dataList.append({
                    'id': i.id,
                    'tableItem': tableItem,
                    'priority': i.priority,
                    'testType': i.testType,
                    'caseName': i.caseName,
                    'pageName': i.page.pageName,
                    'funName': i.fun.funName,
                    'labelId': i.label,
                    'elementdynamic': False,
                    'caseState': i.caseState,
                    'passRate': 0,
                    'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                    "userName": f"{i.uid.userName}({i.uid.nickName})",
                    'createUserName': cls_FindTable.get_userName(i.cuid),
                })
        response['TableData'] = dataList
        response['Total'] = obj_db_CaseBaseData.count()
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


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])  # 当前操作者
        basicData = objData.BasicData
        testSet = objData.TestSet
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_CaseMaintenance', 'data_save', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(
            is_del=0, pid_id=basicData.proId, page_id=basicData.pageId, fun_id=basicData.funId,
            label=basicData.labelId, testType=basicData.testType, caseName=basicData.caseName
        )
        if obj_db_CaseBaseData.exists():
            response['errorMsg'] = f'当前所属功能及同标签同类型下已有相同用例名称,请更改!'
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'UI', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(basicData.proId),
                        cls_FindTable.get_page_name(basicData.pageId),
                        cls_FindTable.get_fun_name(basicData.funId),
                        userId,
                        '【新增用例】', CUFront=responseData
                    )
                    # endregion
                    # region 保存基本信息
                    save_db_CaseBaseData = db_CaseBaseData.objects.create(
                        pid_id=basicData.proId, page_id=basicData.pageId, fun_id=basicData.funId,
                        environmentId_id=basicData.environmentId, testType=basicData.testType,
                        label=basicData.labelId, priority=basicData.priorityId, caseName=basicData.caseName,
                        caseState=basicData.caseState, cuid=userId, uid_id=userId, is_del=0,onlyCode=onlyCode
                    )
                    # endregion
                    # region 历史恢复
                    # restoreData = responseData
                    # restoreData['BasicInfo']['updateTime'] = save_db_CaseBaseData.updateTime.strftime(
                    #     '%Y-%m-%d %H:%M:%S')
                    # restoreData['BasicInfo']['createTime'] = save_db_CaseBaseData.createTime.strftime(
                    #     '%Y-%m-%d %H:%M:%S')
                    # restoreData['BasicInfo']['uid_id'] = save_db_CaseBaseData.uid_id
                    # restoreData['BasicInfo']['cuid'] = save_db_CaseBaseData.cuid
                    # restoreData['onlyCode'] = onlyCode
                    # db_ApiCaseHistory.objects.create(
                    #     pid_id=basicInfo.proId,
                    #     page_id=basicInfo.pageId,
                    #     fun_id=basicInfo.funId,
                    #     case_id=save_db_CaseBaseData.id,
                    #     caseName=basicInfo.caseName,
                    #     onlyCode=onlyCode,
                    #     operationType='Add',
                    #     restoreData=restoreData,
                    #     uid_id=userId
                    # )
                    # endregion
                    # region 关联页面
                    product_list_to_insert = list()
                    for item_page in basicData.associatedPage:
                        product_list_to_insert.append(db_AssociatedPage(
                            case_id=save_db_CaseBaseData.id,
                            page_id=item_page,
                            is_del=0,
                            onlyCode=onlyCode
                        ))
                    db_AssociatedPage.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 测试集
                    product_list_to_insert = list()
                    for item_index, item_testSet in enumerate(testSet, 0):
                        product_list_to_insert.append(db_TestSet(
                            case_id=save_db_CaseBaseData.id,
                            index=item_index,
                            state=1 if item_testSet.state else 0,
                            eventName=item_testSet.eventName,
                            elementId=item_testSet.elementId if item_testSet.elementId else None,
                            elementType=item_testSet.elementType,
                            inputData=item_testSet.inputData if item_testSet.inputData else None,
                            assertType=item_testSet.assertType if item_testSet.assertType else None,
                            assertValueType=item_testSet.assertValueType if item_testSet.assertValueType else None,
                            assertValue=item_testSet.assertValue if item_testSet.assertValue else None,
                            is_del=0,
                            onlyCode=onlyCode
                        ))
                    db_TestSet.objects.bulk_create(product_list_to_insert)
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['statusCode'] = 2001
    return JsonResponse(response)
