# Generated by Django 5.0.7 on 2024-08-25 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CWAdmin', '0005_cwadmin_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cwadmin',
            name='state',
            field=models.CharField(max_length=50),
        ),
    ]
