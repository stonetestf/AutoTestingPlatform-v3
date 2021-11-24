from django.db import models


# Create your models here.
class BasicRole(models.Model):  # 基础角色
    roleName = models.CharField("角色名称", max_length=10, null=True)
    uid = models.ForeignKey("login.UserTable", to_field='id', on_delete=models.CASCADE)
    dataType = models.IntegerField("数据类别(0:系统级别,不可删除/1:普通级别,可删除)", null=False)
    is_del = models.IntegerField("是否删除(0:删除,1:不删除)", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('更新时间', auto_now=True)
