# Generated by Django 4.0.5 on 2022-07-25 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_cards', '0006_alter_taskcardstep_manhours_alter_taskcardstep_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskcardstep',
            options={},
        ),
        migrations.RemoveField(
            model_name='taskcardstep',
            name='number',
        ),
    ]
