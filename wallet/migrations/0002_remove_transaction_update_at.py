# Generated by Django 2.1.5 on 2020-05-24 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='update_at',
        ),
    ]