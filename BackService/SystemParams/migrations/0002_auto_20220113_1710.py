# Generated by Django 2.2.24 on 2022-01-13 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SystemParams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemparams',
            name='remarks',
            field=models.CharField(max_length=100, null=True, verbose_name='备注信息'),
        ),
        migrations.AlterField(
            model_name='systemparams',
            name='valueType',
            field=models.CharField(max_length=10, verbose_name='参数类型(Input,Bool)'),
        ),
    ]
