# Generated by Django 2.2.24 on 2022-01-13 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20211129_1528'),
        ('FunManagement', '0006_funmanagement_onlycode'),
    ]

    operations = [
        migrations.AddField(
            model_name='funhistory',
            name='uid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='login.UserTable'),
            preserve_default=False,
        ),
    ]
