# Generated by Django 2.2.24 on 2021-12-20 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_IntMaintenance', '0015_auto_20211213_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='apibasedata',
            name='requestUrlRadio',
            field=models.IntegerField(default=1, verbose_name='1 2 3 URl备选'),
            preserve_default=False,
        ),
    ]
