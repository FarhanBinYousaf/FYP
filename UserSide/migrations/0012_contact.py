# Generated by Django 4.1.7 on 2023-04-04 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserSide', '0011_remove_jobseeker_confirmpassword'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(max_length=100)),
                ('LastName', models.CharField(max_length=100)),
                ('Email', models.CharField(max_length=100)),
                ('Subject', models.CharField(blank=True, max_length=100, null=True)),
                ('Query', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
