# Generated by Django 5.0.7 on 2024-08-27 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MAdmin', '0002_constituency_admin_assigned'),
    ]

    operations = [
        migrations.AddField(
            model_name='constituency',
            name='district',
            field=models.CharField(default='none', max_length=30),
        ),
    ]
