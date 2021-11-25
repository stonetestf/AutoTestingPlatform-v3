from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction
from django.contrib.auth import hashers

import json

# Create your db here.
from login.models import UserTable as db_UserTable
from django.contrib.auth.models import User as db_DjUser
from routerPar.models import Router as db_Router
from login.models import UserBindRole as db_UserBindRole
from role.models import RoleBindMenu as db_RoleBindMenu
from info.models import OperateInfo as db_OperateInfo
from info.models import PushInfo as db_PushInfo

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker

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
def load_user_info(request):
    response = {}
    try:
        token = request.META['HTTP_TOKEN']
        userId = cls_FindTable.get_userId(token)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', 'home', 'load_user_info', errorMsg)
    else:
        # region 基本信息
        obj_db_UserTable = db_UserTable.objects.filter(id=userId)
        if obj_db_UserTable:
            # region 处理userImg
            fileList = []
            if obj_db_UserTable[0].userImg:
                name = f"{cls_Common.generate_random_value()}.png"
                userImg = eval(obj_db_UserTable[0].userImg)
                base64_to_img = cls_ImageProcessing.base64_to_img(userImg, f"{settings.TEMP_PATH}/{name}")
                if base64_to_img['state']:
                    fileList.append({
                        'name': name,
                        'url': f"{settings.NGINX_SERVER}/Temp/{name}"
                    })
            # endregion
            baseInfo = {
                'userName': obj_db_UserTable[0].userName,
                'nickName': obj_db_UserTable[0].nickName,
                'userImg': str(eval(obj_db_UserTable[0].userImg),
                               encoding='utf-8') if obj_db_UserTable[0].userImg else None,
                'fileList': fileList,
                'emails': obj_db_UserTable[0].emails,
            }
            response['baseInfo'] = baseInfo
            # endregion

            # region 权限信息

            # endregion
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = '用户信息获取失败!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_user_info(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        nickName = request.POST['nickName']
        emails = request.POST['emails']
        password = request.POST['password']

        fileList = cls_Common.conversion_post_lists('fileList', request.POST)
        # deleteFileList = cls_Common.conversion_post_lists('deleteFileList',request.POST)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', 'home', 'save_user_info', errorMsg)
    else:
        obj_db_user = db_UserTable.objects.filter(id=userId)
        if obj_db_user:
            obj_db_DjUser = db_DjUser.objects.get(id=obj_db_user[0].userId)
            if obj_db_DjUser:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        obj_db_DjUser.password = hashers.make_password(password=password)
                        obj_db_DjUser.save()
                        obj_db_user.update(nickName=nickName, emails=emails)

                        # region 处理上传的图片
                        if fileList:
                            name = fileList[0]['name']
                            # url = fileList[0]['url']
                            localhostPath = f"{settings.TEMP_PATH}/{name}"
                            get_file_md5 = cls_Common.get_file_md5(localhostPath)
                            if obj_db_user[0].imgMD5 != get_file_md5:
                                img_to_base64 = cls_ImageProcessing.img_to_base64(localhostPath)
                                obj_db_user.update(userImg=img_to_base64, imgMD5=get_file_md5)
                        else:
                            obj_db_user.update(userImg=None, imgMD5=None)
                        # endregion
                except Exception as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'保存失败:{e}'
                else:
                    response['statusCode'] = 2002
            else:
                response['errorMsg'] = '内置用户信息缺失!'
        else:
            response['errorMsg'] = '未查询到该用户信息'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 获取HOME页面的菜单权限
def get_home_permissions(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', 'home', 'get_home_permissions', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0)
        obj_level_1_Menu = obj_db_Router.filter(level=1, sysType='Home').order_by('sortNum')  # 1级菜单
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0, user_id=userId)
        menuTable = []
        if obj_db_UserBindRole:
            roleId = obj_db_UserBindRole[0].id
            for item_level_1 in obj_level_1_Menu:
                children = []
                # 2级菜单
                obj_level_2_Menu = obj_db_Router.filter(
                    level=2, belogId=item_level_1.id, sysType='Home').order_by('index')
                for item_level_2 in obj_level_2_Menu:
                    obj_db_RoleBindMenu = db_RoleBindMenu.objects.filter(is_del=0, sysType='Home', role_id=roleId)
                    for item_bindMenu in obj_db_RoleBindMenu:
                        if item_bindMenu.router.id == item_level_2.id:
                            children.append({
                                'index': str(item_level_2.index),
                                'menuName': item_level_2.menuName
                            })
                menuTable.append({'index': str(item_level_1.sortNum),
                                  'level': item_level_1.level,
                                  'menuName': item_level_1.menuName,
                                  'disPlay': False if children or item_level_1.menuName == 'Home' else True,
                                  'icon': item_level_1.icon,
                                  'children': children})
        else:
            pass
        response['statusCode'] = 2000
        # response['menuDisPlqy'] = menuDisPlqy
        response['menuTable'] = menuTable
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 返回路由地址
def get_router_path(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)

        sysType = objData.sysType
        index = objData.index
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', 'home', 'get_router_path', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(sysType=sysType, index=index, is_del=0)
        if obj_db_Router:
            response['statusCode'] = 2000
            response['routerPath'] = obj_db_Router[0].routerPath
        else:
            response['errorMsg'] = '未查询到此菜单参数!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 用户统计数据
def get_user_statistics_info(request):
    response = {}
    errorCount = 0
    changeCount = 0
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Home', 'home', 'get_router_path', errorMsg)
    else:
        obj_db_UserTable = db_UserTable.objects.filter(id=userId)
        obj_db_OperateInfo = db_OperateInfo.objects.filter(is_read=0)
        if obj_db_UserTable:
            if obj_db_UserTable[0].userName == 'admin':
                obj_db_PushInfo = db_PushInfo.objects.filter(received=0)
                obj_db_OperateInfo = obj_db_OperateInfo.filter(remindType='Error')
            else:
                obj_db_PushInfo = db_PushInfo.objects.filter(received=0, uid_id=userId)
                obj_db_OperateInfo = obj_db_OperateInfo.filter(uid_id=userId,remindType='Error')
            for i in obj_db_PushInfo:
                match i.oinfo.remindType:
                    case 'Error':
                        errorCount += 1
                    case 'Add' | 'Edit':
                        changeCount += 1
            errorCount += obj_db_OperateInfo.count()
            response['statusCode'] = 2000
            response['message'] = f"当前您有未读信息: <br>错误信息({errorCount}),更变信息({changeCount}),<br>请注意查收!"

    return JsonResponse(response)
