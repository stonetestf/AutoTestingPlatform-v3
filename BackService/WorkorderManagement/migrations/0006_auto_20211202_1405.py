# Generated by Django 2.2.24 on 2021-12-02 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkorderManagement', '0005_auto_20211202_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklifecycle',
            name='operationType',
            field=models.CharField(max_length=10, verbose_name='操作类型(Add,Edit,Close)'),
        ),
    ]