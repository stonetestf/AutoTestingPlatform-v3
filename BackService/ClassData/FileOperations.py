# Create reference here.
from ClassData.Logger import Logging

import os

# Create info here.
cls_Logging = Logging()


# 文件操作
class FileOperations(object):
    def file_to_path(self, fileObj):
        tempPath = f"{os.path.abspath('.')}/_DataFiles/Temp/"
        try:
            with open(tempPath + fileObj.name, 'wb') as f:
                for line in fileObj.chunks():
                    f.write(line)
            FilePath = tempPath + fileObj.name
            return {'state': True, 'filePath': FilePath, 'fileName': fileObj.name}
        except BaseException as e:
            return {'state': False, 'errorMsg': e}

    def read_file(self, filePath):
        results = {}
        try:
            with open(filePath, 'r') as f:
                data = f.read()
        except BaseException as e:
            results['state'] = False
            results['errorMsg'] = f'文件读取失败:{e}'
        else:
            results['state'] = True
            results['data'] = data
        return results
