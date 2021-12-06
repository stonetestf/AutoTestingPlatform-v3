from django.db import models


# Create your models here.
class ApiBaseData(models.Model):
    pid = models.ForeignKey(to='ProjectManagement.ProManagement', to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey(to='PageManagement.PageManagement', to_field='id', on_delete=models.CASCADE)
    fun = models.ForeignKey(to='FunManagement.FunManagement', to_field='id', on_delete=models.CASCADE)
    apiName = models.CharField('接口名称', max_length=100, null=False)
    environment = models.ForeignKey(  # 页面环境
        to='PageEnvironment.PageEnvironment', to_field='id', on_delete=models.CASCADE)
    requestType = models.CharField('请求类型(GET/POST)', max_length=50, null=True)
    requestUrl = models.CharField('请求地址', max_length=500, null=True)
    requestParamsType = models.CharField('请求参数类型(Params、Body)', max_length=10, null=True)  # 此参数必定有
    bodyRequestSaveType = models.CharField('body数据保存类型(none,form-data,json,raw)', max_length=10, null=True)
    apiState = models.CharField("接口状态(InDev,Completed,Discard)", max_length=10, null=False)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)


class ApiHeaders(models.Model):  # 头部参数
    apiId = models.ForeignKey(to='ApiBaseData', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    key = models.CharField('key', max_length=100, null=True)
    value = models.TextField('value', null=True)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)


class ApiParams(models.Model):
    apiId = models.ForeignKey(to='ApiBaseData', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    key = models.CharField('key', max_length=100, null=True)
    value = models.TextField('value', null=True)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)


class ApiBody(models.Model):
    apiId = models.ForeignKey(to='ApiBaseData', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    key = models.CharField('key', max_length=100, null=True)
    value = models.TextField('value/Raw参数/file', null=True)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)


class ApiExtract(models.Model):  # 提取
    apiId = models.ForeignKey(to='ApiBaseData', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    key = models.CharField('key', max_length=100, null=True)
    value = models.TextField('value', null=True)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)


class ApiValidate(models.Model):  # 断言参数
    apiId = models.ForeignKey(to='ApiBaseData', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    checkName = models.CharField('检查值', max_length=100, null=False)
    validateType = models.CharField('断言类型', max_length=50, null=False)
    valueType = models.CharField('断言值类型', max_length=50, null=False)
    expectedResults = models.TextField('预期结果', null=False)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)


class ApiOperation(models.Model):  # 前后置操作
    apiId = models.ForeignKey(to='ApiBaseData', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    location = models.CharField('位置 前/后(Pre,Rear)', max_length=20, null=False)
    operationType = models.CharField('操作类型(Methods,DataBase)', max_length=20, null=False)
    methodsName = models.CharField('函数方法', max_length=100, null=False)
    dataBaseId = models.CharField('要执行的数据库连接ID', max_length=50, null=False)
    sql = models.TextField('Sql数据', null=False)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)