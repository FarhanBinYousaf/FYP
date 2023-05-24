# Generated by Django 4.2.1 on 2023-05-20 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminSide', '0003_ocrjobs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ocrjobs',
            name='Data',
        ),
        migrations.AddField(
            model_name='ocrjobs',
            name='Contact',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ocrjobs',
            name='Date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ocrjobs',
            name='Location',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ocrjobs',
            name='Organization',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]