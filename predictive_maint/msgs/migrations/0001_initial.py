# Generated by Django 4.0.5 on 2022-07-09 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('defects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlembicVersion',
            fields=[
                ('version_num', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'alembic_version',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AcarsMsgRaw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, max_length=10, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('processed', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'acars_msg_raw',
            },
        ),
        migrations.CreateModel(
            name='FaultReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arriving', models.CharField(blank=True, max_length=9, null=True)),
                ('departing', models.CharField(blank=True, max_length=9, null=True)),
                ('flight', models.CharField(blank=True, max_length=9, null=True)),
                ('report_datetime', models.DateTimeField(blank=True, null=True)),
                ('raw', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fault_report', to='msgs.acarsmsgraw')),
            ],
            options={
                'db_table': 'fault_report',
            },
        ),
        migrations.CreateModel(
            name='Fde',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.CharField(blank=True, max_length=3, null=True)),
                ('fde_code', models.CharField(blank=True, max_length=10, null=True)),
                ('fault_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fde_messages', to='msgs.faultreport')),
            ],
            options={
                'db_table': 'fde',
            },
        ),
        migrations.CreateModel(
            name='MessageDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mmsg', models.CharField(max_length=10)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('ata', models.CharField(blank=True, max_length=10, null=True)),
                ('major_notification_name', models.CharField(blank=True, max_length=50, null=True)),
                ('minor_notification_name', models.CharField(blank=True, max_length=50, null=True)),
                ('fim_ref', models.CharField(blank=True, max_length=50, null=True)),
                ('mel_ref', models.CharField(blank=True, max_length=20, null=True)),
                ('criteria', models.CharField(blank=True, max_length=200, null=True)),
                ('tbs_program', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'message_description',
            },
        ),
        migrations.CreateModel(
            name='Plane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tail', models.CharField(max_length=10)),
                ('airline_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'db_table': 'plane',
            },
        ),
        migrations.CreateModel(
            name='PlaneType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'plane_type',
            },
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=30, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('date_time', models.DateTimeField(blank=True, null=True)),
                ('arriving', models.CharField(blank=True, max_length=9, null=True)),
                ('departing', models.CharField(blank=True, max_length=9, null=True)),
                ('flight', models.CharField(blank=True, max_length=9, null=True)),
                ('phase', models.CharField(blank=True, max_length=9, null=True)),
                ('data', models.TextField(blank=True, null=True)),
                ('plane', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='snaphots', to='msgs.plane')),
                ('raw', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='snaphots', to='msgs.acarsmsgraw')),
            ],
            options={
                'db_table': 'snapshot',
            },
        ),
        migrations.AddField(
            model_name='plane',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planes', to='msgs.planetype'),
        ),
        migrations.CreateModel(
            name='Mmsg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mmsg_code', models.CharField(blank=True, max_length=10, null=True)),
                ('msg_date_time', models.DateTimeField(blank=True, null=True)),
                ('chapter', models.CharField(blank=True, max_length=3, null=True)),
                ('section', models.CharField(blank=True, max_length=3, null=True)),
                ('equip_number', models.CharField(blank=True, max_length=20, null=True)),
                ('defect_status', models.CharField(blank=True, default='Not open', max_length=10, null=True)),
                ('defect_ref', models.CharField(blank=True, max_length=20, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('defect', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='defects.defect')),
                ('description', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='maint_message', to='msgs.messagedescription')),
                ('fault_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plf', to='msgs.faultreport')),
                ('fde', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mmsgs', to='msgs.fde')),
            ],
            options={
                'db_table': 'mmsg',
                'ordering': ['-msg_date_time'],
            },
        ),
        migrations.AddField(
            model_name='messagedescription',
            name='plane_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_descriptions', to='msgs.planetype'),
        ),
        migrations.AddField(
            model_name='acarsmsgraw',
            name='plane',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_messages', to='msgs.plane'),
        ),
    ]
