# Generated by Django 5.0.7 on 2024-09-07 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Voter', '0027_alter_votekey_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votekey',
            name='key',
            field=models.BinaryField(),
        ),
    ]
