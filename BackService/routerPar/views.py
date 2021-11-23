from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
# from django.conf import settings
# from django.db import transaction
# from django.contrib.auth import hashers

import json

# Create your db here.
from routerPar.models import Router as db_Router

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
        menuName = objData.menuName
        menuLevel = objData.menuLevel
        sysType = objData.sysType

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', '2', 'routerPar>select_data', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0).order_by('index')
        select_db_RouterPar = obj_db_Router[minSize: maxSize]
        if menuName:
            obj_db_Router = obj_db_Router.filter(menuName__icontains=menuName)
            select_db_RouterPar = obj_db_Router[minSize: maxSize]
        if menuLevel:
            obj_db_Router = obj_db_Router.filter(level=menuLevel)
            select_db_RouterPar = obj_db_Router[minSize: maxSize]
        if sysType:
            obj_db_Router = obj_db_Router.filter(sysType=sysType)
            select_db_RouterPar = obj_db_Router[minSize: maxSize]

        for i in select_db_RouterPar:
            level = "一级菜单" if i.level == 1 else "二级菜单"
            dataList.append(
                {"id": i.id,
                 "levelText": level,
                 "index": i.index,
                 "menuName": i.menuName,
                 "routerPath": i.routerPath,
                 "sysType": i.sysType,
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_Router.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 显示右侧 层级预览图
def get_preview_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home','2','registered',errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0).order_by('sortNum')
        find_db_Router = obj_db_Router.filter(sysType=sysType, level='1')
        for item_router in find_db_Router:
            # 根据1级菜单id,查询二级菜单
            children = []
            select_db_RouterPar = obj_db_Router.filter(belogId=item_router.id)
            for i in select_db_RouterPar:
                children.append({'id': i.id,
                                 'label': i.menuName,
                                 'sortNum': i.sortNum,
                                 'allowDrag': True,  # 能否拖动
                                 'allowDrop': False})  # 能否拖入
            dataList.append({'id': item_router.id, 'label': item_router.menuName, 'allowDrag': False,
                             'children': children})
        response['statusCode'] = 2000
        response['TreeData'] = dataList

    return JsonResponse(response)