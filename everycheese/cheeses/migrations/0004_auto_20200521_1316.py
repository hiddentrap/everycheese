# Generated by Django 3.0.6 on 2020-05-21 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheeses', '0003_cheese_create'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cheese',
            old_name='create',
            new_name='creator',
        ),
    ]