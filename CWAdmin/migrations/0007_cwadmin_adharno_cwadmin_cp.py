# Generated by Django 5.0.7 on 2024-08-26 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CWAdmin', '0006_alter_cwadmin_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='cwadmin',
            name='adharno',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cwadmin',
            name='cp',
            field=models.IntegerField(null=True),
        ),
    ]
