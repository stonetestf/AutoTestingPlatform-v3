# Generated by Django 2.2.24 on 2021-12-02 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0021_auto_20211202_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operateinfo',
            name='triggerType',
            field=models.CharField(max_length=10, verbose_name='触发类型(sys,push)'),
        ),
    ]
