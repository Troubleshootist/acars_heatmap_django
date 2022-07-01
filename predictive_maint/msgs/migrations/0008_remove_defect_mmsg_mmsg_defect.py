# Generated by Django 4.0.5 on 2022-07-01 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('msgs', '0007_defectstatus_alter_defect_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defect',
            name='mmsg',
        ),
        migrations.AddField(
            model_name='mmsg',
            name='defect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='msgs.defect'),
        ),
    ]
