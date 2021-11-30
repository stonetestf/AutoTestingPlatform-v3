from django.db import models


# Create your models here.
class ProManagement(models.Model):
    sysType = models.CharField("所属系统", max_length=10, null=False)
    proName = models.CharField("项目名称", max_length=20, null=False)
    remarks = models.CharField("备注信息", max_length=100, null=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)


class ProBindMembers(models.Model):  # 项目绑定成员
    pid = models.ForeignKey(to='ProManagement', to_field='id', on_delete=models.CASCADE)
    role = models.ForeignKey(to='role.BasicRole', to_field='id', on_delete=models.CASCADE)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
