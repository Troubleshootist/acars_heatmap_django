# Generated by Django 4.0.5 on 2022-06-15 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msgs', '0005_messagedescription_some_test_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagedescription',
            name='some_test_field',
        ),
    ]