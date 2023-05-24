# Generated by Django 4.1.7 on 2023-03-10 19:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserSide', '0007_remove_jobseeker_firstname_remove_jobseeker_lastname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseeker',
            name='password',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(8)]),
        ),
    ]