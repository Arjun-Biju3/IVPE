# Generated by Django 5.0.7 on 2024-08-26 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MAdmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='constituency',
            name='admin_assigned',
            field=models.IntegerField(default=0),
        ),
    ]
