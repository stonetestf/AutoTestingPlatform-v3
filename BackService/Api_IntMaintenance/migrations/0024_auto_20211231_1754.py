# Generated by Django 2.2.24 on 2021-12-31 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_IntMaintenance', '0023_auto_20211231_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apibody',
            name='fileList',
        ),
        migrations.AddField(
            model_name='apibody',
            name='filePath',
            field=models.TextField(null=True, verbose_name='文件保存地址'),
        ),
    ]