# Generated by Django 4.0.5 on 2022-07-29 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msgs', '0001_initial'),
        ('task_cards', '0007_alter_taskcardstep_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcard',
            name='planes',
            field=models.ManyToManyField(related_name='task_cards', to='msgs.plane'),
        ),
    ]
