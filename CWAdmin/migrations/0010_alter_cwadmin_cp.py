# Generated by Django 5.0.7 on 2024-08-26 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CWAdmin', '0009_alter_cwadmin_adharno_alter_cwadmin_cp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cwadmin',
            name='cp',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
