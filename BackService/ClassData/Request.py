# Create your db here.
from Api_TestReport.models import TempExtractData as db_TempExtractData
from GlobalVariable.models import GlobalVariable as db_GlobalVariable
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData
from Api_IntMaintenance.models import ApiHeaders as db_ApiHeaders
from Api_IntMaintenance.models import ApiParams as db_ApiParams
from Api_IntMaintenance.models import ApiBody as db_ApiBody
from Api_IntMaintenance.models import ApiExtract as db_ApiExtract
from Api_IntMaintenance.models import ApiValidate as db_ApiValidate
from PageEnvironment.models import PageEnvironment as db_PageEnvironment

# Create reference here.
from ClassData.Logger import Logging as cls_Logging

import requests
import os
import ast
import json


class RequstOperation(cls_Logging):
    # 循环请求的数据查询出当前请求的最终是从params，body，中哪种发出
    def for_data_get_requset_params_type(self, paramsTable, bodyTable, raw):
        requestParamsType = None
        for item_params in paramsTable:
            if item_params.state:
                requestParamsType = 'Params'
                return requestParamsType
        for item_body in bodyTable:
            if item_body.state:
                requestParamsType = 'Body'
                return requestParamsType
        if raw:
            requestParamsType = 'Body'
            return requestParamsType
        return requestParamsType

    # 转换参数中带有引用的数据
    def conversion_params_import_data(self, proId, requestUrl, requestHeaders, requestData):
        results = {}
        conversionRequestUrl = requestUrl
        conversionHeaders = {}
        conversionRequestData = {}
        if '{{' in requestUrl:
            splitUrl = requestUrl.split('{{')
            globalName = splitUrl[1].replace('}}', '')
            obj_db_GlobalVariable = db_GlobalVariable.objects.filter(
                sysType='API', is_del=0, pid_id=proId, globalName=globalName)
            if obj_db_GlobalVariable:
                conversionRequestUrl = conversionRequestUrl.replace("{{%s}}" % globalName,
                                                                    obj_db_GlobalVariable[0].globalValue)

        for item_headersKey in requestHeaders.keys():
            item_headersValue = requestHeaders[item_headersKey]
            if '{{' in item_headersValue:
                splitHeaders = item_headersValue.split('{{')
                globalName = splitHeaders[1].replace('}}', '')
                obj_db_GlobalVariable = db_GlobalVariable.objects.filter(
                    sysType='API', is_del=0, pid_id=proId, globalName=globalName)
                if obj_db_GlobalVariable:
                    conversionHeaders[item_headersKey] = obj_db_GlobalVariable[0].globalValue
                else:
                    conversionHeaders[item_headersKey] = item_headersValue
            else:
                conversionHeaders[item_headersKey] = item_headersValue

        for item_dataKey in requestData.keys():
            item_dataValue = requestData[item_dataKey]
            if '{{' in item_dataValue:
                splitData = item_dataValue.split('{{')
                globalName = splitData[1].replace('}}', '')
                obj_db_GlobalVariable = db_GlobalVariable.objects.filter(
                    sysType='API', is_del=0, pid_id=proId, globalName=globalName)
                if obj_db_GlobalVariable:
                    conversionRequestData[item_dataKey] = obj_db_GlobalVariable[0].globalValue
                else:
                    conversionRequestData[item_dataKey] = item_dataValue
            else:
                conversionRequestData[item_dataKey] = item_dataValue

        results['state'] = True
        results['requestUrl'] = conversionRequestUrl
        results['headersData'] = conversionHeaders
        results['requestData'] = conversionRequestData
        return results

    # 转换请求数据为JSON格式
    def conversion_params_to_json(self, headers, params, bodyType, body):
        results = {}
        headersDict = {}
        paramsDict = {}
        bodyDict = {}
        for item_headers in headers:
            headersDict[item_headers['key']] = item_headers['value']

        for item_params in params:
            paramsDict[item_params['key']] = item_params['value']

        if bodyType == 'form-data':
            for item_body in body:
                bodyDict[item_body['key']] = item_body['value']
        elif bodyType in ('json', 'raw'):
            pass
        else:
            bodyDict = {}

        results['state'] = True
        results['headersDict'] = headersDict
        results['paramsDict'] = paramsDict
        results['bodyDict'] = bodyDict
        return results

    # 核心-单-获取请求的数据
    def get_request_data(self, apiId, environmentId):
        results = {}
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, id=apiId)
        if obj_db_ApiBaseData:
            # region 获取环境URl
            if environmentId:
                obj_db_PageEnvironment = db_PageEnvironment.objects.filter(id=environmentId)
                if obj_db_PageEnvironment:
                    environmentUrl = obj_db_PageEnvironment[0].environmentUrl
                else:
                    environmentUrl = obj_db_ApiBaseData[0].environment.environmentUrl
            else:
                environmentUrl = obj_db_ApiBaseData[0].environment.environmentUrl
            # endregion
            results['proId'] = obj_db_ApiBaseData[0].pid_id
            results['requestType'] = obj_db_ApiBaseData[0].requestType
            results['requestUrl'] = f"{environmentUrl}{obj_db_ApiBaseData[0].requestUrl}"
            results['requestParamsType'] = obj_db_ApiBaseData[0].requestParamsType  # 最终是以body请求还是以params请求
            # 如果是body请求，还要看他请求的类型来决定以哪种形式发送
            results['bodyRequestType'] = obj_db_ApiBaseData[0].bodyRequestSaveType

            # region 请求数据获取
            # 获取头部数据
            obj_db_ApiHeaders = db_ApiHeaders.objects.filter(is_del=0, apiId_id=apiId)
            results['headersData'] = [{'key': i.key, 'value': i.value} for i in obj_db_ApiHeaders if i.state]

            # 获取params数据
            obj_db_ApiParams = db_ApiParams.objects.filter(is_del=0, apiId_id=apiId)
            results['paramsData'] = [{'key': i.key, 'value': i.value} for i in obj_db_ApiParams if i.state]

            # 获取body数据
            obj_db_ApiBody = db_ApiBody.objects.filter(is_del=0, apiId_id=apiId)
            if results['bodyRequestType'] == 'form-data':
                results['bodyData'] = [{'key': i.key, 'value': i.value} for i in obj_db_ApiBody if i.state]
            elif results['bodyRequestType'] in ('json', 'raw'):
                results['bodyData'] = obj_db_ApiBody[0].value
            else:
                results['bodyData'] = []

            # 获取提取数据
            obj_db_ApiExtract = db_ApiExtract.objects.filter(is_del=0, apiId_id=apiId)
            results['extractData'] = [{'key': i.key, 'value': i.value} for i in obj_db_ApiExtract if i.state]

            # 获取断言数据
            obj_db_ApiValidate = db_ApiValidate.objects.filter(is_del=0, apiId_id=apiId)
            results['validateData'] = [{'checkName': i.checkName, 'validateType': i.validateType,
                                        'valueType': i.valueType, 'expectedResults': i.expectedResults}
                                       for i in obj_db_ApiValidate if i.state]

            # 获取前置数据

            # 获取后置数据


            # endregion
            results['state'] = True
        else:
            results['state'] = False
            results['errorMsg'] = '没有找到当前所发送请求的接口信息'
        return results

    # 转换参数为最后请求的数据
    def conversion_data_to_request_data(self, getRequestData):
        results = {'state': False}
        proId = getRequestData['proId']
        requestUrl = getRequestData['requestUrl']

        requestParamsType = getRequestData['requestParamsType']
        headersData = getRequestData['headersData']
        paramsData = getRequestData['paramsData']
        bodyRequestType = getRequestData['bodyRequestType']
        bodyData = getRequestData['bodyData']

        # 转换请求数据为JSON格式
        conversionToJson = self.conversion_params_to_json(
            headersData, paramsData, bodyRequestType, bodyData)
        if conversionToJson['state']:
            requestHeaders = conversionToJson['headersDict']
            requestParams = conversionToJson['paramsDict']
            requestBody = conversionToJson['bodyDict']
            if requestParamsType == "Body":
                requestData = requestBody
                results['requestData'] = bodyData
            else:
                requestData = requestParams
                results['requestData'] = paramsData

            # 转换参数中带有引用的数据
            conversionImportData = self.conversion_params_import_data(
                proId, requestUrl, requestHeaders, requestData)
            if conversionImportData['state']:
                conversionRequestUrl = conversionImportData['requestUrl']
                conversionHeadersData = conversionImportData['headersData']
                conversionRequestData = conversionImportData['requestData']
                results['state'] = True
                results['conversionRequestUrl'] = conversionRequestUrl
                results['conversionHeadersData'] = conversionHeadersData
                results['conversionRequestData'] = conversionRequestData
            else:
                results['errorMsg'] = conversionImportData['errorMsg']
        else:
            # 这里目前没有可获取到的错误，以后在需求中添加
            results['errorMsg'] = ""
        return results

    # 核心-单-请求
    def requests_api(self, requestType, requestParamsType, bodyRequestType, url, headers, requestData, files=None):
        """
        :param requestType: GET/POST
        :param requestParamsType: Params,Body 2种请求参数方式
        param bodyRequestType: none,form-data,json,raw 3种请求参数方式
        :param url: 拼接好的整URL
        :param headers:
        :param requestData:
        :param files:
        :return:执行返回的数据结果
        """
        timeout = 10
        r = {}
        results = {}
        os.system('echo 3 > /proc/sys/vm/drop_caches')  # 执行前清理缓存
        cls_Logging.print_log(self, 'info', 'requests_api', f'RequestURl:{url}')
        cls_Logging.print_log(self, 'info', 'requests_api', f'requestType:{requestType}')
        cls_Logging.print_log(self, 'info', 'requests_api', f'requestParamsType:{requestParamsType}')
        cls_Logging.print_log(self, 'info', 'requests_api', f'requestParamsType:{bodyRequestType}')
        cls_Logging.print_log(self, 'info', 'requests_api', f'headers:{headers}')
        cls_Logging.print_log(self, 'info', 'requests_api', f'requestData:{requestData}')
        cls_Logging.print_log(self, 'info', 'requests_api', f'files:{files}')

        try:
            if requestType == "GET":
                r = requests.get(url, headers=headers, params=requestData, timeout=timeout)
            elif requestType == "POST":
                file = {'file': open(files.url, 'rb')} if files else {}
                if bodyRequestType in ("form-data", "raw", 'none'):
                    r = requests.post(url, headers=headers, data=requestData, files=file, timeout=timeout)
                else:  # json
                    requestData = json.dumps(requestData)
                    r = requests.post(url, headers=headers, params=requestData, files=file, timeout=timeout)
            else:
                message = f"当前使用了未录入的请求参数:{requestType}"
                results['state'] = False
                results['errorMsg'] = message
                cls_Logging.print_log(self, 'error', 'requests_api', message)
                cls_Logging.record_error_info(self, 'API', 'ClassData', 'requests_api', message)
        except BaseException as e:
            message = f"请求失败:{e}"
            results['state'] = False
            results['errorMsg'] = message
            cls_Logging.print_log(self, 'error', 'requests_api', message)
            cls_Logging.record_error_info(self, 'API', 'ClassData', 'requests_api', message)
        else:
            text = r.text
            if '<!DOCTYPE html>' in text:
                content = text
            elif '<html>' in text:
                content = text
            elif not text:
                content = text
            else:
                if 'null' in text:
                    text = text.replace('null', "''")
                else:
                    text = r.text
                try:
                    text = json.dumps(json.loads(text), ensure_ascii=False)
                    if 'true' in text:
                        text = text.replace('true', 'True')
                    if 'false' in text:
                        text = text.replace('false', 'False')
                    content = ast.literal_eval(text)
                except BaseException as e:
                    content = text
                    cls_Logging.print_log(self, 'error', 'requests_api', f'content:{e}')
            cls_Logging.print_log(self, 'info', 'requests_api', f'content:{content}')
            results['state'] = True
            results['responseCode'] = r.status_code
            results['time'] = round(r.elapsed.total_seconds(), 2)
            responseHeaders = [{'key': item_resHeaders,
                                'value': r.headers[item_resHeaders]}
                               for item_resHeaders in r.headers]
            results['responseHeaders'] = responseHeaders
            results['content'] = content
            return results

    # 执行提取和断言操作
    def perform_extract_and_validate(self,onlyCode,extractData,validateData,requestsApi,userId):
        results = {'extractTable':[],
                   'assertionTable':[]}
        if extractData:  # 如果有提取的数据才会执行断言
            requestExtract = self.request_extract(userId, onlyCode,
                                                  requestsApi['content'],
                                                  requestsApi['responseCode'],
                                                  extractData)
            if requestExtract['state']:
                results['extractTable'] = requestExtract['extractList']

                # 断言数据
                requestValidate = self.request_validate(requestExtract['extractList'],
                                                        validateData)
                if requestValidate['state']:
                    results['assertionTable'] = requestValidate['validateReport']
                    results['reportState'] = 'Pass' if requestValidate['reportState'] else 'Fail'
                    results['state'] = True
                else:
                    results['errorMsg'] = requestValidate['errorMsg']
                    results['state'] = False
            else:
                results['errorMsg'] = requestExtract['errorMsg']
                results['state'] = False
        else:
            results['reportState'] = 'Pass'
            results['state'] = True
        return results

    # 核心-单接口的执行
    def run_request(self, apiId, environmentId, onlyCode, userId):
        results = {
            'tabPane': {
                'requsetHeaders': [],  # 原始请求头
                'content': "",  # 返回主体
                'responseHeaders': [],  # 返回头部
                'extractTable': [],  # 提取信息
                'assertionTable': []  # 断言信息
            },
            'state': False
        }
        getRequestData = self.get_request_data(apiId, environmentId)
        if getRequestData['state']:
            results['originalUrl'] = getRequestData['requestUrl']
            results['tabPane']['requsetHeaders'] = getRequestData['headersData']
            requestParamsType = getRequestData['requestParamsType']
            bodyRequestType = getRequestData['bodyRequestType']
            extractData = getRequestData['extractData']
            validateData = getRequestData['validateData']
            requestType = results['requestType'] = getRequestData['requestType']

            # 转换参数为最后请求的数据
            conversionDataToRequestData = self.conversion_data_to_request_data(getRequestData)
            if conversionDataToRequestData['state']:
                results['tabPane']['requestData'] = conversionDataToRequestData['requestData']
                conversionRequestUrl = results['requestUrl'] = conversionDataToRequestData['conversionRequestUrl']
                conversionHeadersData = conversionDataToRequestData['conversionHeadersData']
                conversionRequestData = conversionDataToRequestData['conversionRequestData']
                # 发送请求
                requestsApi = self.requests_api(
                    requestType, requestParamsType, bodyRequestType,
                    conversionRequestUrl, conversionHeadersData, conversionRequestData)
                if requestsApi['state']:
                    results['responseCode'] = requestsApi['responseCode']
                    results['time'] = requestsApi['time']
                    # 解决中文乱码的问题
                    results['tabPane']['content'] = json.dumps(
                        requestsApi['content'], sort_keys=True, indent=4, separators=(",", ": "),
                        ensure_ascii=False)
                    results['tabPane']['responseHeaders'] = requestsApi['responseHeaders']

                    # 断言及提取
                    performExtractAndValidate = self.perform_extract_and_validate(
                        onlyCode,extractData,validateData,requestsApi,userId)
                    if performExtractAndValidate['state']:
                        results['tabPane']['extractTable'] = performExtractAndValidate['extractTable']
                        results['tabPane']['assertionTable'] = performExtractAndValidate['assertionTable']
                        results['reportState'] = performExtractAndValidate['reportState']
                    else:
                        results['errorMsg'] = performExtractAndValidate['errorMsg']
                    results['state'] = True
                else:
                    results['errorMsg'] = requestsApi['errorMsg']
            else:
                results['errorMsg'] = conversionDataToRequestData['errorMsg']
        else:
            results['errorMsg'] = getRequestData['errorMsg']
        return results

    # def run_request(self, apiId, environmentId, onlyCode, userId):
    #     results = {
    #         'tabPane': {
    #             'requsetHeaders': [],  # 原始请求头
    #             'content': "",  # 返回主体
    #             'responseHeaders': [],  # 返回头部
    #             'extractTable': [],  # 提取信息
    #             'assertionTable': []  # 断言信息
    #         },
    #         'state': False
    #     }
    #     getRequestData = self.get_request_data(apiId, environmentId)
    #     if getRequestData['state']:
    #         proId = getRequestData['proId']
    #         requestUrl = results['originalUrl'] = getRequestData['requestUrl']
    #         requestType = results['requestType'] = getRequestData['requestType']
    #         requestParamsType = getRequestData['requestParamsType']
    #         headersData = results['tabPane']['requsetHeaders'] = getRequestData['headersData']
    #         paramsData = getRequestData['paramsData']
    #         bodyRequestType = getRequestData['bodyRequestType']
    #         bodyData = getRequestData['bodyData']
    #         extractData = getRequestData['extractData']
    #         validateData = getRequestData['validateData']
    #         # 转换请求数据为JSON格式
    #         conversionToJson = self.conversion_params_to_json(
    #             headersData, paramsData, bodyRequestType, bodyData)
    #         if conversionToJson['state']:
    #             requestHeaders = conversionToJson['headersDict']
    #             requestParams = conversionToJson['paramsDict']
    #             requestBody = conversionToJson['bodyDict']
    #             if requestParamsType == "Body":
    #                 requestData = requestBody
    #                 results['tabPane']['requestData'] = bodyData
    #             else:
    #                 requestData = requestParams
    #                 results['tabPane']['requestData'] = paramsData
    #
    #             # 转换参数中带有引用的数据
    #             conversionImportData = self.conversion_params_import_data(
    #                 proId, requestUrl, requestHeaders, requestData)
    #             if conversionImportData['state']:
    #                 conversionRequestUrl = results['requestUrl'] = conversionImportData['requestUrl']
    #                 conversionHeadersData = conversionImportData['headersData']
    #                 conversionRequestData = conversionImportData['requestData']
    #
    #                 # 发送请求
    #                 requestsApi = self.requests_api(
    #                     requestType, requestParamsType, bodyRequestType,
    #                     conversionRequestUrl, conversionHeadersData, conversionRequestData)
    #                 if requestsApi['state']:
    #                     results['responseCode'] = requestsApi['responseCode']
    #                     results['time'] = requestsApi['time']
    #                     # 解决中文乱码的问题
    #                     results['tabPane']['content'] = json.dumps(
    #                         requestsApi['content'], sort_keys=True, indent=4, separators=(",", ": "),
    #                         ensure_ascii=False)
    #                     results['tabPane']['responseHeaders'] = requestsApi['responseHeaders']
    #                     if extractData:  # 如果有提取的数据才会执行断言
    #                         requestExtract = self.request_extract(userId, onlyCode,
    #                                                               requestsApi['content'],
    #                                                               requestsApi['responseCode'],
    #                                                               extractData)
    #                         if requestExtract['state']:
    #                             results['tabPane']['extractTable'] = requestExtract['extractList']
    #
    #                             # 断言数据
    #                             requestValidate = self.request_validate(requestExtract['extractList'],
    #                                                                     validateData)
    #                             if requestValidate['state']:
    #                                 results['tabPane']['assertionTable'] = requestValidate['validateReport']
    #                                 results['reportState'] = 'Pass' if requestValidate['reportState'] else 'Fail'
    #                         else:
    #                             results['errorMsg'] = requestExtract['errorMsg']
    #                     else:
    #                         results['reportState'] = 'Pass'
    #                     results['state'] = True
    #                 else:
    #                     results['errorMsg'] = requestsApi['errorMsg']
    #             else:
    #                 results['errorMsg'] = conversionImportData['errorMsg']
    #         else:
    #             # 这里目前没有可获取到的错误，以后在需求中添加
    #             results['errorMsg'] = ""
    #     else:
    #         results['errorMsg'] = getRequestData['errorMsg']
    #     return results

    # 提取
    def request_extract(self, userId, onlyCode, content, statuscode, extract):
        results = {}
        extractList = []

        if type(content) == dict:
            for item in extract:
                extractKey = item['key']
                extractValue = item['value']
                retValue = None  # 返回结果值
                if extractKey == 'statuscode':
                    retValue = statuscode
                else:
                    if extractValue[:2] == '$.':
                        params = extractValue[2:]
                        splitParams = params.split('.')
                        if len(splitParams) == 1:
                            combination_content = f'content["{params}"]'
                        else:
                            combination_content = f'content'
                            for item in splitParams:
                                splitItem = item.split('[')
                                combination_content += f'["{splitItem[0]}"]'
                                if len(splitItem) > 1:
                                    combination_content += f'[{splitItem[1][:-1]}]'
                        try:
                            retValue = eval(combination_content)
                        except:
                            # 能进这里的肯定是设置了无法被提取到的参数
                            message = f"提取失败:无法提取到:{combination_content}," \
                                      f"下的返回值,请确认Response返回值中有此数据!"
                            results['state'] = False
                            results['errorMsg'] = message
                            cls_Logging.print_log(self, 'warning', 'requests_api', message)

                            # region 添加操作信息
                            operationInfo = cls_Logging.record_local_operation_info(
                                self, 'API', 'System', 2, 'Warning',
                                None, 'ClassData', 'request_extract', message,
                            )
                            cls_Logging.push_to_user(self, operationInfo, userId)
                            # endregion
                    else:
                        message = f"提取失败:变量名称:{extractKey}," \
                                  f"的提取表达式:{extractValue},首参数不为$,请更改后在重试!"
                        results['state'] = False
                        results['errorMsg'] = message
                        cls_Logging.print_log(self, 'error', 'requests_api', message)
                        cls_Logging.record_error_info(self, 'API', 'ClassData', 'request_extract', message)
                if type(retValue) == str:
                    retValueType = 'str'
                elif type(retValue) == list:
                    retValueType = 'list'
                elif type(retValue) == int:
                    retValueType = 'int'
                elif type(retValue) == float:
                    retValueType = 'float'
                elif type(retValue) == bool:
                    retValueType = 'bool'
                else:
                    retValueType = ''
                extractList.append({'key': extractKey, 'value': retValue, 'valueType': retValueType})

                # 保存进临时数据库中
                db_TempExtractData.objects.create(
                    onlyCode=onlyCode, keys=extractKey, values=retValue, valueType=retValueType
                )
        else:
            results['state'] = False
            results['errorMsg'] = f"使用了未录入的提取类型:{type(content)}"
        if 'errorMsg' not in results:
            cls_Logging.print_log(self, 'info', 'request_extract', f'返回提取数据:{extractList}')
            results['state'] = True
            results['extractList'] = extractList
        return results

    # 断言
    def request_validate(self, extractList, validate):
        results = {}
        validateReport = []
        reportState = True
        for item_validate in validate:
            checkName = item_validate['checkName']  # 检查值
            validateType = item_validate['validateType']
            valueType = eval(item_validate['valueType'])
            expectedResults = item_validate['expectedResults']  # 预期结果

            if valueType == str:
                retValueType = "Str"
            elif valueType == int:
                retValueType = "Int"
            elif valueType == list:
                retValueType = "List"
            else:
                retValueType = ""

            for item_extract in extractList:
                extractKey = item_extract['key']
                extractValue = item_extract['value']
                extractValueType = eval(item_extract['valueType'])
                if extractKey == checkName:
                    if validateType == 'equals':  # ==
                        if valueType == list:
                            try:
                                list_expected = eval(expectedResults)
                            except BaseException as e:
                                reportState = False
                            else:
                                if list_expected == extractValue:
                                    reportState = True
                                else:
                                    reportState = False
                        else:
                            try:  # 可能会出现 int(str)这种的断言,所以这里要捕获这种错误
                                if valueType(expectedResults) == extractValueType(extractValue):
                                    reportState = True
                                else:
                                    reportState = False
                            except:
                                reportState = False
                    elif validateType == 'contains':  # in
                        if str(expectedResults) in str(extractValue):
                            reportState = True
                        else:
                            reportState = False
                    elif validateType == 'not_equals':  # !=
                        if valueType(expectedResults) != extractValueType(extractValue):
                            reportState = True
                        else:
                            reportState = False

                    if extractValueType == str:
                        extractValueType = "Str"
                    elif extractValueType == int:
                        extractValueType = "Int"
                    elif extractValueType == list:
                        extractValueType = "List"
                    validateReport.append(
                        {'checkName': checkName,
                         'retCheckOut': f'{retValueType}({expectedResults})',  # 预期结果
                         'validateType': validateType,
                         'retExtractorOut': f'{extractValueType}({extractValue})',  # 实际返回
                         'results': reportState}
                    )
                    break
            else:
                validateReport.append(
                    {'checkName': checkName,
                     'retCheckOut': f'{retValueType}({expectedResults})',  # 预期结果
                     'validateType': validateType,
                     'retExtractorOut': '没有找到当前检查值的可提取数据,请检查提取设置中是否有此检查值!',
                     'results': False}
                )
        passNum = 0
        failNum = 0
        for i in validateReport:
            if i['results']:
                passNum += 1
            else:
                failNum += 1
        results['state'] = True
        results['validateReport'] = validateReport
        results['reportState'] = False if failNum >= 1 else True
        cls_Logging.print_log(self, 'info', 'request_validate', f'返回断言数据:{validateReport}')
        return results
