# Generated by Django 4.0.5 on 2022-07-02 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msgs', '0010_defecthistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagedescription',
            name='fim_ref',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]