from django.db import models


# Create your models here.
class ProManagement(models.Model):
    sysType = models.CharField("所属系统:Api", max_length=10, null=False)
    proName = models.CharField("项目名称",max_length=20, null=False)
    remarks = models.CharField("备注信息", max_length=100, null=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    createTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserBindRole', to_field='id', on_delete=models.CASCADE)  # 用户Id
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)",null=False)