from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction
from django.contrib.auth import hashers
from dwebsocket.decorators import accept_websocket
from time import sleep

import json
import psutil

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
        cls_Logging.record_error_info('HOME', 'home', 'load_user_info', errorMsg)
    else:
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
        cls_Logging.record_error_info('HOME', 'home', 'save_user_info', errorMsg)
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
        cls_Logging.record_error_info('HOME', 'home', 'get_home_permissions', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0)
        obj_level_1_Menu = obj_db_Router.filter(level=1, sysType='Home').order_by('sortNum')  # 1级菜单
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0, user_id=userId)
        menuTable = []
        if obj_db_UserBindRole:
            roleId = obj_db_UserBindRole[0].role_id
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
@require_http_methods(["GET"])  # 获取API页面的菜单权限
def get_api_permissions(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'home', 'get_api_permissions', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0)
        obj_level_1_Menu = obj_db_Router.filter(level=1, sysType='API').order_by('sortNum')  # 1级菜单
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0, user_id=userId)
        menuTable = []
        if obj_db_UserBindRole:
            roleId = obj_db_UserBindRole[0].role_id
            for item_level_1 in obj_level_1_Menu:
                children = []
                # 2级菜单
                obj_level_2_Menu = obj_db_Router.filter(
                    level=2, belogId=item_level_1.id, sysType='API').order_by('index')
                for item_level_2 in obj_level_2_Menu:
                    obj_db_RoleBindMenu = db_RoleBindMenu.objects.filter(is_del=0, sysType='Api', role_id=roleId)
                    for item_bindMenu in obj_db_RoleBindMenu:
                        if item_bindMenu.router.id == item_level_2.id:
                            children.append({
                                'index': str(item_level_2.index),
                                'menuName': item_level_2.menuName,
                                'path':item_level_2.routerPath,
                            })
                menuTable.append({'index': str(item_level_1.sortNum),
                                  'level': item_level_1.level,
                                  'menuName': item_level_1.menuName,
                                  'disPlay': False if children or item_level_1.menuName == 'HOME' else True,
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
        cls_Logging.record_error_info('HOME', 'home', 'get_router_path', errorMsg)
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
@require_http_methods(["GET"])  # 用户统计数据,首页右下角弹出框
def get_user_statistics_info(request):
    response = {}
    errorCount = 0
    changeCount = 0
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'get_router_path', errorMsg)
    else:
        obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId, is_del=0)
        obj_db_OperateInfo = db_OperateInfo.objects.filter(is_read=0)
        obj_db_PushInfo = db_PushInfo.objects.filter(uid_id=userId)
        if obj_db_UserBindRole:
            if obj_db_UserBindRole[0].role.dataType == 0:  # 系统级别角色可以理解为超级管理
                obj_db_OperateInfo = obj_db_OperateInfo.filter(remindType='Error')
            else:
                obj_db_OperateInfo = obj_db_OperateInfo.filter(uid_id=userId, remindType='Warning')
            for i in obj_db_PushInfo:
                if i.oinfo.remindType == 'Error' and i.oinfo.is_read == 0:
                    errorCount += 1
                elif i.oinfo.remindType in ('Add', 'Edit') and i.oinfo.is_read == 0:
                    changeCount += 1
            errorCount += obj_db_OperateInfo.count()
            response['statusCode'] = 2000
            response['message'] = f"当前您的信息: <br>错误信息({errorCount}),更变推送信息({changeCount}),<br>请注意查收!"

    return JsonResponse(response)


@accept_websocket  # 获取服务器的性能,服务的状态,当前用户推送统计数量
def get_server_indicators(request):
    counter = 0  # 计数器 到10就会断开通信
    if request.is_websocket():
        retMessage = str(request.websocket.wait(), 'utf-8')  # 接受前段发送来的数据
        if retMessage:
            objData = object_maker(json.loads(retMessage))
            token = objData.Params.token
            if objData.Message == "Start":  # 开始执行
                while True:
                    sendText = {}
                    try:
                        retMessage = request.websocket.read()
                    except BaseException as e:
                        cls_Logging.print_log('info', 'get_server_indicators', f'前端已关闭,断开连接:{e}')
                        break
                    else:
                        if retMessage:
                            objData = object_maker(json.loads(retMessage))
                            if objData.Message == 'Heartbeat':
                                counter = 0
                            else:
                                counter += 1
                                if counter >= 10:
                                    request.websocket.close()
                                    cls_Logging.print_log('info', 'get_server_indicators',
                                                          f'心跳包:{counter}秒内无响应,断开连接')
                                    break
                            userId = cls_FindTable.get_userId(token)
                            obj_db_PushInfo = db_PushInfo.objects.filter(uid_id=userId)
                            pushCount = obj_db_PushInfo.count()
                            # region CPU和内存
                            cpu = psutil.cpu_percent(interval=2)
                            mem = psutil.virtual_memory()[2]
                            # endregion
                            # region Celery
                            celery = False
                            celeryBeat = False
                            perform_Celery = cls_Common.run_command("ps -ef |grep worker",False)
                            debug_worker = []  # 在Debug模式下有点奇葩所以要计数下
                            for i in perform_Celery:
                                if "celery -A BackGround worker -l info" in i:
                                    celery = True
                                    break
                                elif "celery worker -A BackGround -E --loglevel=INFO" in i:  # Debug模式
                                    debug_worker.append(i)
                                    if len(debug_worker) >= 3:
                                        celery = True
                                        break
                            perform_CeleryBeat = cls_Common.run_command("ps -ef |grep beat",False)
                            for i in perform_CeleryBeat:
                                if "celery -A BackGround beat -l info" in i:
                                    celeryBeat = True
                                    break
                                elif "celery beat -A BackGround --loglevel=INFO" in i:  # Debug模式
                                    celeryBeat = True
                                    break

                            # endregion
                            sendText = {
                                'pushCount': pushCount,
                                'cpu': cpu,
                                'mem': mem,
                                'celery':celery,
                                'celeryBeat':celeryBeat,
                            }

                        request.websocket.send(json.dumps(sendText, ensure_ascii=False).encode('utf-8'))
                        sleep(1)
