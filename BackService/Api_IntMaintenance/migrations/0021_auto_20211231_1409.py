# Generated by Django 2.2.24 on 2021-12-31 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_IntMaintenance', '0020_apibasedata_assignedtouser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apihistory',
            name='apiName',
            field=models.CharField(max_length=100, verbose_name='页面名称'),
        ),
    ]
