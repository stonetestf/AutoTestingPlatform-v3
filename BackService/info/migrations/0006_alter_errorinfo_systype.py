# Generated by Django 3.2.9 on 2021-11-23 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0005_auto_20211123_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorinfo',
            name='sysType',
            field=models.CharField(max_length=10, verbose_name='系统类型(API/UI/PTS/ALL)'),
        ),
    ]
