# Generated by Django 4.1.7 on 2023-03-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserSide', '0004_jobseeker_confirmpassword_jobseeker_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseeker',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
    ]
