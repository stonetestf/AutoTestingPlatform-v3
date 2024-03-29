# Generated by Django 2.2.24 on 2021-12-08 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0008_auto_20211129_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sysType', models.CharField(max_length=10, verbose_name='所属系统')),
                ('globalType', models.IntegerField(verbose_name='变量类型(0:普通变量,)')),
                ('globalName', models.CharField(max_length=100, null=True, verbose_name='变量名称')),
                ('globalValue', models.TextField(null=True, verbose_name='变量值')),
                ('remarks', models.TextField(null=True, verbose_name='备注')),
                ('createTime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('cuid', models.IntegerField(verbose_name='创建者用户')),
                ('is_del', models.IntegerField(verbose_name='是否删除(1:删除,0:不删除)')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.UserTable')),
            ],
        ),
    ]
