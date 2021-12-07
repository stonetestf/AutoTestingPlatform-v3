from django.db import models


# Create your models here.
class TempExtractData(models.Model):  # 保存临时提出并转换后的数据
    onlyCode = models.CharField('唯一随机ID', max_length=100, null=True)
    keys = models.CharField('key', max_length=100, null=True)
    values = models.TextField('value', null=True)
    valueType = models.CharField('值类型', max_length=50, null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
