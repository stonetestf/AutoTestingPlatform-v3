# Generated by Django 2.2.24 on 2022-01-21 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ui_ElementMaintenance', '0004_elementhistory_element'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementbasedata',
            name='elementState',
            field=models.IntegerField(default=1, verbose_name='是否启用(1:启用,0:禁用)'),
            preserve_default=False,
        ),
    ]
