# Generated by Django 2.2.24 on 2022-01-21 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ui_ElementMaintenance', '0003_elementhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementhistory',
            name='element',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Ui_ElementMaintenance.ElementBaseData'),
            preserve_default=False,
        ),
    ]
