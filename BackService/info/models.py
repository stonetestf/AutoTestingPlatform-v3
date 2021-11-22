from django.db import models


# Create your models here.
class ErrorInfo(models.Model):  # 错误日志
    sys = models.CharField('系统类型(Login/Int/Fun/Per)', max_length=10, null=False)
    level = models.IntegerField("错误级别", null=False)
    methodName = models.CharField('方法名称', max_length=100, null=False)
    info = models.TextField('报错信息', null=True)
    is_read = models.IntegerField("是否删除(0:未读,1:已读)", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)


class OperateInfo(models.Model):  # 操作日志
    sysType = models.CharField('系统类型(Int/Fun/Per)', max_length=10, null=False)
    toPage = models.CharField('所属页面', max_length=100, null=False)
    toFun = models.CharField('所属功能', max_length=100, null=False)
    CUFront = models.TextField('修改前信息', null=True)
    CURear = models.TextField('修改后信息', null=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)
    createTime = models.DateTimeField('创建时间', auto_now=True)
