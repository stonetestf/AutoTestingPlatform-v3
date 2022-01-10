from django.db import models


# Create your models here.
class ApiBatchTask(models.Model):
    pid = models.ForeignKey(to='ProjectManagement.ProManagement', to_field='id', on_delete=models.CASCADE)  # 项目id
    batchName = models.CharField('任务名称', max_length=20, null=False)
    priority = models.CharField("优先级(P0-P3)", max_length=10, null=False)
    pushTo = models.CharField('接收邮件', max_length=100, null=True)
    remarks = models.TextField("备注信息", null=True)
    hookId = models.CharField('钩子ID，是一个随机码的唯一值', max_length=100, null=False)
    hookState = models.IntegerField("是否开启(0:未开启,1:开启)", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    cuid = models.IntegerField("创建人", null=False)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    is_del = models.IntegerField("是否删除(0:删除,1:不删除)", null=False)


class ApiBatchTaskTestSet(models.Model):  # 定时任务排序数据
    batchTask = models.ForeignKey(to='ApiBatchTask', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("排序", null=False)
    task = models.ForeignKey(to='Api_TimingTask.ApiTimingTask', to_field='id', on_delete=models.CASCADE)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    is_del = models.IntegerField("是否删除(0:删除,1:不删除)", null=False)
