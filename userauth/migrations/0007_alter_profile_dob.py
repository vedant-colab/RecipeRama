# Generated by Django 4.1.1 on 2023-08-05 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0006_alter_profile_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
