# Generated by Django 2.2.24 on 2022-01-05 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20211129_1528'),
        ('WorkorderManagement', '0008_worklifecycle_is_del'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(null=True, verbose_name='工单信息')),
                ('createTime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.UserTable')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorkorderManagement.WorkorderManagement')),
            ],
        ),
    ]