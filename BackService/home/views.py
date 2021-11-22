from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings

# Create your db here.
from login.models import UserTable as db_UserTable

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing

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
        cls_Logging.record_error_info('API', '1', 'home>load_user_info', errorMsg)
    else:
        # region 基本信息
        obj_db_UserTable = db_UserTable.objects.filter(id=userId)
        if obj_db_UserTable:
            # region 处理userImg
            fileList = []
            if obj_db_UserTable[0].userImg:
                name = f"{cls_Common.generate_random_value()}.png"
                imgByte64 = eval(obj_db_UserTable[0].imgByte64)
                base64_to_img = cls_ImageProcessing.base64_to_img(imgByte64, f"{settings.TEMP_PATH}/{name}")
                if base64_to_img['state']:
                    fileList.append({
                        'name': name,
                        'url': f"{settings.NGINX_SERVER}/Temp/{name}"
                    })
            # endregion
            baseInfo = {
                'userName': obj_db_UserTable[0].userName,
                'nickName': obj_db_UserTable[0].nickName,
                'userImg': obj_db_UserTable[0].userImg,
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
    response['errorMsg'] = ""
    try:
        nickName = request.POST['nickName']
        emails = request.POST['emails']
        password = request.POST['password']

        fileList = cls_Common.conversion_post_lists('fileList',request.POST)
        deleteFileList = cls_Common.conversion_post_lists('deleteFileList',request.POST)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', '2', 'home>save_user_info', errorMsg)
    else:
        pass
    #     find_db_user = db_user.objects.filter(id=userId)
    #     if find_db_user:
    #         # 修改用户密码
    #         find_db_djuser = db_djuser.objects.get(id=find_db_user[0].userId)
    #         if find_db_djuser:
    #             find_db_djuser.password = hashers.make_password(password=password)
    #             find_db_djuser.save()
    #             find_db_user.update(nickName=nickName, emails=emails)
    #             if fileList:
    #                 name = fileList[0]['name']
    #                 url = fileList[0]['url']
    #                 if url.split('/')[-2] == 'Temp':
    #                     localhostPath = f"{settings.BASE_DIR}/UpLoad/Temp/{name}"
    #                 else:
    #                     localhostPath = f"{settings.BASE_DIR}/UpLoad/UserImages/{userId}/{name}"
    #                 get_file_md5 = cls_ComClass.get_file_md5(localhostPath)
    #                 img_to_base64 = cls_ImageProcessing.img_to_base64(localhostPath)
    #                 find_db_user.update(imgByte64=img_to_base64,imgMD5=get_file_md5)
    #             else:
    #                 find_db_user.update(imgByte64=None, imgMD5=None)
    #         else:
    #             response['errorMsg'] = '内置用户信息缺失!'
    #     else:
    #         response['errorMsg'] = '未查询到该用户信息'
    # if not response['errorMsg']:
    #     response['statusCode'] = 2002
    return JsonResponse(response)
