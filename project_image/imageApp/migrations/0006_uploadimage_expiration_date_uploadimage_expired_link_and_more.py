# Generated by Django 4.2.6 on 2023-10-11 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageApp', '0005_rename_image_300_uploadimage_image_400'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadimage',
            name='expiration_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='uploadimage',
            name='expired_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='uploadimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
