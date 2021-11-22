from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.FileOperations import FileOperations

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_FileOperations = FileOperations()


# Create your views here.
@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def upLoad_to_temp_path(request):
    response = {}
    try:
        fileObj = request.FILES.get('file', None)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', '2', 'upLoad>upLoad_to_temp_path', errorMsg)
    else:
        if fileObj:
            toTemp = cls_FileOperations.file_to_path(fileObj)
            if toTemp['state']:
                fileName = toTemp['fileName']
                filePath = toTemp['filePath']
                response['file'] = {'filePath': filePath, 'fileName': fileName}
                response['statusCode'] = 2001
            else:
                response['errorMsg'] = toTemp['errorMsg']
        else:
            response['errorMsg'] = f"没有获取到上传文件"
    return JsonResponse(response)
