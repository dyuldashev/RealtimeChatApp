# Generated by Django 5.1.4 on 2025-01-04 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='preferred_language',
            field=models.CharField(blank=True, choices=[('uzb', 'Uzbek'), ('ru', 'Russian'), ('en', 'English')], default='en', max_length=3, null=True),
        ),
    ]
