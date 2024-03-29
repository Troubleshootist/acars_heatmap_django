# Generated by Django 4.0.5 on 2022-07-09 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'defect',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DefectStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'defect_status',
            },
        ),
        migrations.CreateModel(
            name='DefectHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('after_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='after_history', to='defects.defectstatus')),
                ('before_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='before_history', to='defects.defectstatus')),
                ('defect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='defects.defect')),
            ],
            options={
                'db_table': 'defect_history',
            },
        ),
    ]
