# Generated by Django 5.0.6 on 2024-09-01 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CWAdmin', '0016_remove_candidate_p_district'),
        ('Voter', '0024_alter_loginkey_key_alter_loginkey_salt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted_at', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_profile', to='CWAdmin.candidate')),
                ('vote', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Voter.votekey')),
            ],
        ),
    ]
