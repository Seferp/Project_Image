# Generated by Django 4.2.6 on 2023-10-15 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imageApp', '0009_remove_uploadimage_expiration_date2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadimage',
            old_name='expiration_date',
            new_name='added_date',
        ),
    ]