# Generated by Django 3.0.8 on 2020-12-21 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_event_guest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='youtube',
            old_name='titel',
            new_name='title',
        ),
    ]
