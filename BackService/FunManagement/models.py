from django.db import models


# Create your models here.
class FunManagement(models.Model):  # 功能管理
    sysType = models.CharField("所属系统", max_length=10, null=False)
    pid = models.ForeignKey("ProjectManagement.ProManagement", to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey("PageManagement.PageManagement", to_field='id', on_delete=models.CASCADE)
    funName = models.CharField('功能名称', max_length=50, null=False)
    remarks = models.CharField("备注信息", max_length=100, null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    is_del = models.IntegerField("是否删除(0:删除,1:不删除)", null=False)
