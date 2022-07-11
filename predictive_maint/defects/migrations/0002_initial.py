# Generated by Django 4.0.5 on 2022-07-09 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('defects', '0001_initial'),
        ('msgs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='defect',
            name='plane',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='defects', to='msgs.plane'),
        ),
        migrations.AddField(
            model_name='defect',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defects', to='defects.defectstatus'),
        ),
    ]
