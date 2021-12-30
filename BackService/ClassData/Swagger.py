from ClassData.Logger import Logging as cls_Logging
from ClassData.FileOperations import FileOperations

import ast

cls_FileOperations = FileOperations()


class Swagger(cls_Logging):
    # 处理JSON文件转换为列表类型
    def analysisJsonData(self, filePath):
        results = {}
        readFile = cls_FileOperations.read_file(filePath)# 读取文件
        if readFile['state']:
            jsonStr = readFile['data']
            jsonStr = ast.literal_eval(jsonStr.replace('true', "True").replace('false', "False"))
            pathJson = jsonStr['paths']

            jsonTable = self.json_to_table(pathJson)
            if jsonTable['state']:
                results['state'] = True
                results['dataTable'] = jsonTable['dataTable']
            else:
                results['state'] = False
                results['errorMsg'] = jsonTable['errorMsg']
        else:
            results['state'] = False
            results['errorMsg'] = readFile['errorMsg']
        return results

    def json_to_table(self,jsonData):
        results = {}
        dataTable = []
        passType = ['delete', 'put']
        try:
            for i in jsonData:
                requestUrl = i
                for k, v in jsonData[i].items():
                    headersData = []  # 头部请求
                    requestData = []  # 主体请求
                    apiName = v['summary']
                    requestType = k
                    bodyRequestTypeTxt = None

                    # region 请求参数类型 Params,body 目前只做2个
                    if requestType == 'get':
                        requestParamsType = 'Params'
                    else:
                        requestParamsType = 'Body'
                    # endregion
                    if requestType not in passType:
                        parameters = v['parameters']
                        requestBody = v['requestBody'] if 'requestBody' in v else []

                        # region 筛选出header 参数
                        for item_header in parameters:
                            if item_header['in'] == 'header':
                                key = item_header['name']  # key值
                                value = item_header[
                                    'example'] if 'example' in item_header else None  # Swagger 所有的VALUE值都是None
                                remarks = item_header['description'] if 'description' in item_header else None  # 描述
                                headersData.append({'key': key, 'value': value, 'remarks': remarks})
                        # endregion
                        # region 筛选出主体 参数
                        if requestType == "get":
                            for item_params in parameters:
                                if item_params['in'] != 'header':
                                    key = item_params['name']  # key值
                                    value = item_params[
                                        'example'] if 'example' in item_params else None  # Swagger 所有的VALUE值都是None
                                    remarks = item_params['description'] if 'description' in item_params else None  # 描述

                                    requestData.append({'key': key, 'value': value, 'remarks': remarks})
                        else:
                            bodyRequestType = None
                            content = requestBody['content']
                            for item_body in content:
                                bodyRequestType = item_body
                            if bodyRequestType == "multipart/form-data":
                                bodyRequestTypeTxt = 'form-data'
                            elif bodyRequestType == "application/x-www-form-urlencoded":
                                bodyRequestTypeTxt = 'x-www-form-urlencoded'
                            elif bodyRequestType == "application/json":
                                bodyRequestTypeTxt = 'json'
                            elif bodyRequestType == "text/plain":
                                bodyRequestTypeTxt = 'raw'
                            else:
                                bodyRequestTypeTxt = None

                            if bodyRequestType in ["multipart/form-data", "application/x-www-form-urlencoded"]:
                                properties = content[bodyRequestType]['schema']['properties']  # body的请求参数
                                for item_body in properties:
                                    # 这2种form-data类型这样获取
                                    key = item_body  # key值
                                    value = properties[item_body]['example'] if 'example' in properties[
                                        item_body] else None  # Swagger 所有的VALUE值都是None
                                    remarks = properties[item_body]['description'] if 'description' in properties[
                                        item_body] else None  # 描述

                                    requestData.append({'key': key, 'value': value, 'remarks': remarks})
                            else:
                                # 一般到这里的都是JSON格式的了
                                value = content[bodyRequestType]['example']  # body的请求参数
                                requestData = {'key': None, 'value': value, 'remarks': None}
                        # endregion
                        dataTable.append({
                            'apiName':apiName,
                            'requestUrl':requestUrl,
                            'requestType':requestType.upper(),
                            'requestParamsType':requestParamsType,
                            'bodyRequestType':bodyRequestTypeTxt,
                            'request':{
                                'headersDataList':headersData,
                                'requestDataList':requestData,
                            }
                        })
        except BaseException as e:
            results['state'] = False
            results['errorMsg'] = f"文件解析失败:{e}"
        else:
            results['state'] = True
            results['dataTable'] = dataTable
        return results