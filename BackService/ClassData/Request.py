class RequstOperation(object):
    # 循环请求的数据查询出当前请求的最终是从params，body，中哪种发出
    def for_data_get_requset_params_type(self, paramsTable, bodyTable,raw):
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