# Generated by Django 4.1.1 on 2023-06-17 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0003_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='', upload_to='profile_pictures/'),
        ),
    ]