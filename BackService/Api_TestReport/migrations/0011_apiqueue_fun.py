# Generated by Django 2.2.24 on 2021-12-15 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FunManagement', '0004_funhistory_fun'),
        ('Api_TestReport', '0010_apiqueue_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiqueue',
            name='fun',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='FunManagement.FunManagement'),
            preserve_default=False,
        ),
    ]
