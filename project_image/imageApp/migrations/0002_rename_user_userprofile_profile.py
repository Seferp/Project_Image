# Generated by Django 4.2.6 on 2023-10-05 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imageApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user',
            new_name='profile',
        ),
    ]
