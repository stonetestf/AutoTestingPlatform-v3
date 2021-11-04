from django.db import models


# Create your models here.
class UserTable(models.Model):
    userId = models.IntegerField("内置用户ID", null=False)  # Dango内置的用户，因为要用到token数据
    userName = models.CharField(max_length=50, null=False)
    nickName = models.CharField(max_length=200, null=False)
    userImg = models.CharField(max_length=100, null=True)
    imgMD5 = models.CharField(max_length=100, null=True)
    emails = models.CharField(max_length=100, null=True)
    is_lock = models.IntegerField("是否锁定(0:不锁定,1:锁定)", null=False)
    is_activation = models.IntegerField("是否激活(0:未激活,1:已激活)", null=False)
    is_del = models.IntegerField(null=False, verbose_name="是否删除(0:不删除,1:删除)")
    createTime = models.DateTimeField('登录时间', auto_now=True)


class ErrorMsg(models.Model):
    sys = models.CharField('测试类型(Login/Int/Fun/Per)', max_length=10, null=False)
    level = models.IntegerField("错误级别", null=False)
    methodName = models.CharField('方法名称', max_length=100, null=False)
    info = models.TextField('报错信息', null=True)
    is_read = models.IntegerField("是否删除(0:未读,1:已读)", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
