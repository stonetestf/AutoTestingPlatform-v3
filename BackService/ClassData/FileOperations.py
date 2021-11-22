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
