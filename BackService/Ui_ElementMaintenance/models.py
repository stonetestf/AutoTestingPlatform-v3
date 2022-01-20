from django.db import models


# Create your models here.
class ElementBaseData(models.Model):
    pid = models.ForeignKey(to='ProjectManagement.ProManagement', to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey(to='PageManagement.PageManagement', to_field='id', on_delete=models.CASCADE)
    fun = models.ForeignKey(to='FunManagement.FunManagement', to_field='id', on_delete=models.CASCADE)
    elementName = models.CharField('元素名称', max_length=100, null=False)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 最后更新者
    cuid = models.IntegerField("创建者用户", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码', max_length=100, null=False)


class ElementLocation(models.Model):  # 元素定位表
    element = models.ForeignKey(to='ElementBaseData', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    targetingType = models.CharField('定位类型', max_length=20, null=False)
    targetingPath = models.CharField('定位地址', max_length=500, null=False)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)
    onlyCode = models.CharField('历史记录唯一码', max_length=100, null=False)
