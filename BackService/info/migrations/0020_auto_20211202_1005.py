# Generated by Django 2.2.24 on 2021-12-02 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0019_auto_20211201_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='operateinfo',
            name='triggerType',
            field=models.CharField(default=1, max_length=10, verbose_name='触发类型(sys,push)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='operateinfo',
            name='level',
            field=models.IntegerField(verbose_name='提醒等级(错误(1),警告(2),新增/修改/删除(3))'),
        ),
    ]
