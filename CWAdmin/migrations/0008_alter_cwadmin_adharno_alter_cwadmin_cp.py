# Generated by Django 5.0.7 on 2024-08-26 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CWAdmin', '0007_cwadmin_adharno_cwadmin_cp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cwadmin',
            name='adharno',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='cwadmin',
            name='cp',
            field=models.IntegerField(),
        ),
    ]
