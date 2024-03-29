# Generated by Django 2.2.24 on 2021-12-20 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('PageEnvironment', '0002_auto_20211208_1146'),
        ('PageManagement', '0005_pagehistory'),
        ('ProjectManagement', '0013_auto_20211213_1048'),
        ('FunManagement', '0004_funhistory_fun'),
        ('login', '0008_auto_20211129_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseBaseData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testType', models.CharField(max_length=20, verbose_name='测试类型(UnitTest:单元,HybridTest:混合)')),
                ('label', models.CharField(max_length=20, verbose_name='用例标签(CommonCase:普通 ReturnCase:BUG回归)')),
                ('priority', models.CharField(max_length=10, verbose_name='优先级(P0-P3)')),
                ('caseName', models.CharField(max_length=50, verbose_name='用例名称')),
                ('caseState', models.CharField(max_length=10, verbose_name='用例状态(InDev:研发中,Completed:已完成,Discard:弃用)')),
                ('createTime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('cuid', models.IntegerField(verbose_name='创建者用户')),
                ('is_del', models.IntegerField(verbose_name='是否删除(1:删除,0:不删除)')),
                ('environmentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PageEnvironment.PageEnvironment')),
                ('fun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FunManagement.FunManagement')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PageManagement.PageManagement')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProjectManagement.ProManagement')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.UserTable')),
            ],
        ),
    ]
