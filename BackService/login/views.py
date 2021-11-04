from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import auth
from django.db import transaction

import json

# Create your views here.
from django.contrib.auth.models import User as db_DjUser
from login.models import UserTable as db_UserTable


# Create reference here.
from ClassData.Logger import Logging

# Create info here.
cls_Logging = Logging()


# Create your views here.
@cls_Logging.log
@require_http_methods(["POST"])  # 外部注册
def registered(request):
    response = {}
    try:
        userName = request.POST['userName']
        passWord = request.POST['passWord']
        nickName = request.POST['nickName']
        emails = request.POST['emails']
    except Exception as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('Login','2','registered',errorMsg)
    else:
        find_db_UserTable = db_UserTable.objects.filter(userName=userName, is_del=1)
        if find_db_UserTable:
            response['errorMsg'] = '已有相同用户名注册,请更换用户名!'
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    create_DjUser = db_DjUser.objects.create_user(username=userName, password=passWord)
                    # is_activation 默认未激活，需要联系管理员进行配置权限工作
                    db_UserTable.objects.create(
                        userId=create_DjUser.id,userName=userName,nickName=nickName,emails=emails,
                        is_lock=1,is_activation=0,is_del=1
                    )
            except Exception as e:  # 自动回滚，不需要任何操作
                errorMsg = f'用户注册失败：{e}!'
                response['errorMsg'] = errorMsg
                cls_Logging.record_error_info('Login', '1', 'registered', errorMsg)
            else:
                response['statusCode'] = 2001
    return JsonResponse(response)
