# Create reference here.
from ClassData.Logger import Logging
from ClassData.Common import Common

import os

# Create info here.
cls_Logging = Logging()
cls_Common = Common()


# 文件操作
class FileOperations(object):
    def file_to_path(self, fileObj):
        tempPath = f"{os.path.abspath('.')}/_DataFiles/Temp/"
        try:
            splitStr = fileObj['file'].name.split('.')
            if len(splitStr) >= 2:
                fileSuffix = splitStr[-1]
            else:
                fileSuffix = ""
            if fileSuffix:
                fileName = f'{cls_Common.generate_only_code()}.{fileSuffix}'
            else:
                fileName = cls_Common.generate_only_code()
            fliePath = f'{tempPath}{fileName}'
            with open(fliePath, 'wb') as f:
                # with open(tempPath + fileObj.name, 'wb') as f:
                for line in fileObj['file'].chunks():
                    f.write(line)
            # FilePath = tempPath + fileObj.name
            return {'state': True, 'filePath': fliePath, 'fileName': fileName}
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
