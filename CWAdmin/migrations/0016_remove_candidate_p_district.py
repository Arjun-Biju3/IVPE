# Generated by Django 5.0.7 on 2024-08-29 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CWAdmin', '0015_remove_candidate_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='p_District',
        ),
    ]
