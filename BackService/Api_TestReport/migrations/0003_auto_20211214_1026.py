# Generated by Django 2.2.24 on 2021-12-14 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_TestReport', '0002_apireport_apireportitem_apitestreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apireport',
            name='reportStatus',
            field=models.CharField(max_length=10, verbose_name='测试报告状态(Pass,Fail,Error)'),
        ),
    ]