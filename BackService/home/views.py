from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction
from django.contrib.auth import hashers
from dwebsocket.decorators import accept_websocket
from time import sleep

import json
import operator
import psutil

# Create your db here.
from django.db.models import Q
from login.models import UserTable as db_UserTable
from django.contrib.auth.models import User as db_DjUser
from routerPar.models import Router as db_Router
from login.models import UserBindRole as db_UserBindRole
from role.models import RoleBindMenu as db_RoleBindMenu
from info.models import OperateInfo as db_OperateInfo
from info.models import PushInfo as db_PushInfo
from Api_TestReport.models import ApiTestReport as db_ApiTestReport
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData
from PageManagement.models import PageManagement as db_PageManagement
from Api_TestReport.models import ApiQueue as db_ApiQueue
from Api_TestReport.models import ApiReportItem as db_ApiReportItem
from Api_CaseMaintenance.models import CaseBaseData as db_CaseBaseData

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
        if obj_db_UserTable.exists():
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
        responseData = json.loads(request.body)
        objData = object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        nickName = objData.nickName
        emails = objData.emails
        password = objData.password
        fileList = objData.fileList
        # deleteFileList = cls_Common.conversion_post_lists('deleteFileList',request.POST)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'save_user_info', errorMsg)
    else:
        obj_db_user = db_UserTable.objects.filter(id=userId)
        if obj_db_user.exists():
            obj_db_DjUser = db_DjUser.objects.get(id=obj_db_user[0].userId)
            if obj_db_DjUser.exists():
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
        if obj_db_UserBindRole.exists():
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
        if obj_db_UserBindRole.exists():
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
                                'path': item_level_2.routerPath,
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
        if obj_db_Router.exists():
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
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'get_router_path', errorMsg)
    else:
        obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId, is_del=0)
        if obj_db_UserBindRole.exists():
            pushCount = db_PushInfo.objects.filter(~Q(oinfo__uid_id=userId), uid_id=userId, is_read=0).count()
            errorCount = db_OperateInfo.objects.filter(remindType='Error', is_read=0).count()
            # warningCount = db_OperateInfo.objects.filter(uid_id=userId, remindType='Warning').count()
            warningCount = db_PushInfo.objects.filter(uid_id=userId, oinfo__remindType='Warning', is_read=0).count()

            if obj_db_UserBindRole[0].role.is_admin == 1:
                message = f"当前您的信息: <br>" \
                          f"错误信息({errorCount}),警告信息({warningCount}),推送信息({pushCount}),<br>" \
                          f"请注意查收!"
            else:
                message = f"当前您的信息: <br>" \
                          f"警告信息({warningCount}),推送信息({pushCount}),<br>" \
                          f"请注意查收!"
            response['statusCode'] = 2000
            response['message'] = message

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
                            obj_db_PushInfo = db_PushInfo.objects.filter(uid_id=userId, is_read=0)
                            pushCount = obj_db_PushInfo.count()
                            # region CPU和内存
                            cpu = psutil.cpu_percent(interval=2)
                            mem = psutil.virtual_memory()[2]
                            # endregion
                            # region Celery
                            celery = False
                            celeryBeat = False
                            perform_Celery = cls_Common.run_command("ps -ef |grep worker", False)
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
                            perform_CeleryBeat = cls_Common.run_command("ps -ef |grep beat", False)
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
                                'celery': celery,
                                'celeryBeat': celeryBeat,
                            }

                        request.websocket.send(json.dumps(sendText, ensure_ascii=False).encode('utf-8'))
                        sleep(1)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 测试结果总览
def api_pagehome_select_test_results(request):
    response = {}
    passData = []
    failData = []
    errorData = []
    reportTime = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_select_test_results', errorMsg)
    else:
        # 这里因该把删除的也显示出来
        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(pid_id=proId).order_by('updateTime')
        for i in obj_db_ApiTestReport:
            reportTime.append(str(i.updateTime.strftime('%Y-%m-%d')))
        reportTime = list(set(reportTime))  # 去重复时间
        reportTime.sort()  # 排序
        for i in reportTime:
            passTotal = 0
            failTotal = 0
            errorTotal = 0
            staTime = i + " 00:00:00"
            endTime = i + " 23:59:59"
            select_db_ApiTestReport = obj_db_ApiTestReport.filter(updateTime__gte=staTime, updateTime__lte=endTime)
            for item in select_db_ApiTestReport:
                if item.reportStatus == 'Pass':
                    passTotal += 1
                elif item.reportStatus == 'Fail':
                    failTotal += 1
                elif item.reportStatus == 'Error':
                    errorTotal += 1
                else:
                    errorTotal += 1
            if passTotal != 0:
                passData.append({'name': i, 'value': [i, passTotal]})
            if failTotal != 0:
                failData.append({'name': i, 'value': [i, failTotal]})
            if errorTotal != 0:
                errorData.append({'name': i, 'value': [i, errorTotal]})

        response['statusCode'] = 2000
        response['timeData'] = reportTime
        response['passData'] = passData
        response['failData'] = failData
        response['errorData'] = errorData
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 项目下的所有数据总统计
def api_pagehome_select_pro_statistical(request):
    response = {}
    dataTable = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_select_pro_statistical', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(is_del=0, pid_id=proId)
        for item_page in obj_db_PageManagement:
            # region 获取本周时间
            weekData = cls_Common.get_this_weeks_interval_data()
            staTime = weekData[0].strftime('%Y-%m-%d') + " 00:00:00"
            endTime = weekData[1].strftime('%Y-%m-%d') + " 23:59:59"
            # endregion
            obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, pid_id=proId, page_id=item_page.id)
            apiTotal = obj_db_ApiBaseData.count()  # 接口数量
            # region 本周新增
            weekTotal = obj_db_ApiBaseData.filter(createTime__gte=staTime, createTime__lte=endTime).count()
            # endregion
            # region 本周执行
            performWeekTotal = db_ApiQueue.objects.filter(
                pid_id=proId, page_id=item_page.id, updateTime__gte=staTime, updateTime__lte=endTime).count()
            # endregion
            perforHistoryTotal = db_ApiQueue.objects.filter(pid_id=proId, page_id=item_page.id).count()  # 历史执行
            obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0,page_id=item_page.id)
            dataTable.append({
                'pageName': item_page.pageName,
                'apiTotal': apiTotal,
                'unitAndCaseTotal':f'{obj_db_CaseBaseData.filter(testType="UnitTest").count()}/'
                                   f'{obj_db_CaseBaseData.filter(testType="HybridTest").count()}',
                'caseTotal':obj_db_CaseBaseData.count(),
                'weekTotal': weekTotal,
                'performWeekTotal': performWeekTotal,
                'perforHistoryTotal': perforHistoryTotal

            })
        response['dataTable'] = dataTable
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 过去7天内Top10
def api_pagehome_select_Formerly_data(request):
    response = {}
    dataTable = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_select__Formerly_data', errorMsg)
    else:
        # region 获取本周时间
        weekData = cls_Common.get_this_weeks_interval_data()
        staTime = weekData[0].strftime('%Y-%m-%d') + " 00:00:00"
        endTime = weekData[1].strftime('%Y-%m-%d') + " 23:59:59"
        # endregion
        # 这里把删除的也显示出来,觉得被删除的一般都是引起系统错误的也算统计内
        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(
            ~Q(reportStatus='Pass'), pid_id=proId, updateTime__gte=staTime, updateTime__lte=endTime)
        reportNameList = [i.reportName for i in obj_db_ApiTestReport]
        reportNameList = list(set(reportNameList))
        for item_reportName in reportNameList:
            failTotal = 0
            errorTotal = 0
            select_db_ApiTestReport = obj_db_ApiTestReport.filter(reportName=item_reportName)
            for i in select_db_ApiTestReport:
                if i.reportStatus == 'Fail':
                    failTotal += 1
                elif i.reportStatus == 'Error':
                    errorTotal += 1
                elif i.reportStatus == '':
                    errorTotal += 1

            if select_db_ApiTestReport[0].reportType == 'API':
                obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=select_db_ApiTestReport[0].taskId)
                if obj_db_ApiBaseData.exists():
                    itsName = f"{obj_db_ApiBaseData[0].page.pageName}/{obj_db_ApiBaseData[0].fun.funName}"
                else:
                    itsName = ""
            elif select_db_ApiTestReport[0].reportType == 'CASE':
                obj_db_CaseBaseData = db_CaseBaseData.objects.filter(id=select_db_ApiTestReport[0].taskId)
                if obj_db_CaseBaseData.exists():
                    itsName = f"{obj_db_CaseBaseData[0].page.pageName}/{obj_db_CaseBaseData[0].fun.funName}"
                else:
                    itsName = ""
            else:
                itsName = ""
            dataTable.append({
                'index': '',
                'itsName': itsName,
                'taskType': select_db_ApiTestReport[0].reportType,
                'taskName': item_reportName,
                'number': failTotal + errorTotal
            })
        dataTable = sorted(dataTable, key=operator.itemgetter('number'), reverse=True)  # 利用number来倒序排列
        # 给index 来赋值
        for index, i in enumerate(dataTable[:10], 1):
            dataTable[index - 1]['index'] = str(index)

        response['dataTable'] = dataTable
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 项目队列
def api_pagehome_select_pro_queue(request):
    response = {}
    dataTable = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_select_pro_queue', errorMsg)
    else:
        obj_db_ApiQueue = db_ApiQueue.objects.filter(~Q(queueStatus='2'), pid_id=proId).order_by('-updateTime')
        for i in obj_db_ApiQueue:
            if i.taskType == 'API':
                obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=i.taskId)
                if obj_db_ApiBaseData.exists():
                    itsName = f"{obj_db_ApiBaseData[0].page.pageName}/{obj_db_ApiBaseData[0].fun.funName}"
                else:
                    itsName = ""
            elif i.taskType == 'CASE':
                obj_db_CaseBaseData = db_CaseBaseData.objects.filter(id=i.taskId)
                if obj_db_CaseBaseData.exists():
                    itsName = f"{obj_db_CaseBaseData[0].page.pageName}/{obj_db_CaseBaseData[0].fun.funName}"
                else:
                    itsName = ""
            else:
                itsName = ""
            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=i.testReport_id)
            dataTable.append({
                'id': i.id,
                'itsName': itsName,
                'taskType': i.taskType,
                'taskName': i.testReport.reportName,
                'taskState': i.queueStatus,
                'performProgress': f"{obj_db_ApiReportItem.count()}/{i.testReport.apiTotal}",
                'updateTime': str(i.updateTime.strftime('%H:%M:%S')),
            })
        response['dataTable'] = dataTable
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 修改队列状态
def api_pagehome_handle_state(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        queueId = request.POST['queueId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_handle_state', errorMsg)
    else:
        db_ApiQueue.objects.filter(id=queueId).update(
            queueStatus=2, updateTime=cls_Common.get_date_time(), uid_id=userId
        )
        response['statusCode'] = 2002
    return JsonResponse(response)
