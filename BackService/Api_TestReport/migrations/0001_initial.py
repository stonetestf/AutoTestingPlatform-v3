# Generated by Django 2.2.24 on 2021-12-07 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TempExtractData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('onlyCode', models.CharField(max_length=100, null=True, verbose_name='唯一随机ID')),
                ('keys', models.CharField(max_length=100, null=True, verbose_name='key')),
                ('values', models.TextField(null=True, verbose_name='value')),
                ('valueType', models.CharField(max_length=50, null=True, verbose_name='值类型')),
                ('createTime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
        ),
    ]
