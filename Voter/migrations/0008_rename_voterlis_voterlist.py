# Generated by Django 5.0.7 on 2024-08-06 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Voter', '0007_voterlis_delete_status_voterlis_eligibility_status_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VoterLis',
            new_name='VoterList',
        ),
    ]
