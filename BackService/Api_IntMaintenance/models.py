from django.db import models


# Create your models here.
class ApiBaseData(models.Model):
    pid = models.ForeignKey(to='ProjectManagement.ProManagement', to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey(to='PageManagement.PageManagement', to_field='id', on_delete=models.CASCADE)
    fun = models.ForeignKey(to='FunManagement.FunManagement', to_field='id', on_delete=models.CASCADE)
    apiName = models.CharField('接口名称', max_length=100, null=False)
    # 页面环境
    environment = models.ForeignKey(to='PageEnvironment.PageEnvironment', to_field='id', on_delete=models.CASCADE)
    requestType = models.CharField('请求类型(GET/POST)', max_length=50, null=True)
    requestUrl = models.CharField('请求地址', max_length=500, null=True)
    requestParamsType = models.CharField('请求参数类型(Params、Body)', max_length=10, null=True)  # 此参数必定有
    bodyRequestSaveType = models.CharField('body数据保存类型(none,form-data,json,raw)', max_length=10, null=True)
    apiState = models.IntegerField("接口状态(InDev,Completed,Discard)", null=False)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
