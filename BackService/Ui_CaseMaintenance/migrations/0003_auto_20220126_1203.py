# Generated by Django 2.2.24 on 2022-01-26 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ui_CaseMaintenance', '0002_uitestset'),
    ]

    operations = [
        migrations.AddField(
            model_name='uiassociatedpage',
            name='onlyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码,新增的时候会创建1个'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uicasebasedata',
            name='onlyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码,新增的时候会创建1个'),
            preserve_default=False,
        ),
    ]