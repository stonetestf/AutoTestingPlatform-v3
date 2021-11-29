from django.db import models


# Create your models here.
class OperateInfo(models.Model):  # 操作日志
    sysType = models.CharField('系统类型(ALL(所有系统通用)/LOGIN/HOME/API/UI/PTS)', max_length=10, null=False)
    level = models.IntegerField("提醒等级(错误(1),警告(2),新增和修改(3),其他(4))", null=False)
    remindType = models.CharField('提醒类别 Error,Warning,Change(Add,Edit),Other', max_length=10, null=False)
    toPage = models.CharField('所属页面', max_length=100, null=True)
    toFun = models.CharField('所属功能', max_length=100, null=True)
    info = models.TextField('报错信息', null=True)
    CUFront = models.TextField('修改前信息', null=True)
    CURear = models.TextField('修改后信息', null=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 创建者
    # beingPushedUid = models.IntegerField("被推送者", null=True)
    is_read = models.IntegerField("是否删除(0:未读,1:已读)", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('更新时间', auto_now=True)


class PushInfo(models.Model):  # 推送表，谁给我推送了1条操作日志
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 被推的人
    oinfo = models.ForeignKey(to='OperateInfo', to_field='id', on_delete=models.CASCADE)  # 操作日志ID
    # received = models.IntegerField("已接收(0:未接收,1:已接收)", null=False)  # 这里只有读取后才会改正
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('更新时间', auto_now=True)
