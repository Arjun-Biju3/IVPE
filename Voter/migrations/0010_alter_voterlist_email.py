# Generated by Django 5.0.7 on 2024-08-11 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Voter', '0009_voterlist_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voterlist',
            name='email',
            field=models.CharField(max_length=50),
        ),
    ]
