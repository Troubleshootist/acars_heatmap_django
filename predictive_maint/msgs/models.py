# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AcarsMsgRaw(models.Model):
    filename = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    airplane = models.CharField(max_length=10, blank=True, null=True)
    processed = models.IntegerField(blank=True, null=True)
    plane = models.ForeignKey(
        'Plane', on_delete=models.CASCADE, related_name='raw_messages')

    class Meta:
        db_table = 'acars_msg_raw'


class Airline(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'airline'


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class FaultReport(models.Model):
    arriving = models.CharField(max_length=9, blank=True, null=True)
    departing = models.CharField(max_length=9, blank=True, null=True)
    flight = models.CharField(max_length=9, blank=True, null=True)
    report_datetime = models.DateTimeField(blank=True, null=True)
    raw = models.ForeignKey(AcarsMsgRaw, on_delete=models.CASCADE,
                            related_name='fault_report', blank=True, null=True)
    plane = models.ForeignKey('Plane', on_delete=models.CASCADE,
                              related_name='fault_reports', blank=True, null=True)

    class Meta:
        db_table = 'fault_report'


class Fde(models.Model):
    cat = models.CharField(max_length=3, blank=True, null=True)
    fde_code = models.CharField(max_length=10, blank=True, null=True)
    fault_report = models.ForeignKey(
        FaultReport, on_delete=models.CASCADE, related_name='fde_messages')
    # mmsg = models.ForeignKey('Mmsg', on_delete=models.CASCADE,
    #                          related_name='fde_message', blank=True, null=True)

    # plf = models.ForeignKey('FdeMmsg', on_delete=models.CASCADE, related_name='fde_messages')

    class Meta:
        db_table = 'fde'


class MessageDescription(models.Model):
    mmsg = models.CharField(max_length=10)
    description = models.CharField(max_length=200, blank=True, null=True)
    ata = models.CharField(max_length=10, blank=True, null=True)
    major_notification_name = models.CharField(
        max_length=50, blank=True, null=True)
    minor_notification_name = models.CharField(
        max_length=50, blank=True, null=True)
    fim_ref = models.CharField(max_length=20, blank=True, null=True)
    mel_ref = models.CharField(max_length=20, blank=True, null=True)
    criteria = models.CharField(max_length=200, blank=True, null=True)
    tbs_program = models.CharField(max_length=200, blank=True, null=True)
    plane_type = models.ForeignKey('PlaneType', on_delete=models.CASCADE,
                                   related_name='message_descriptions', blank=True, null=True)

    class Meta:
        db_table = 'message_description'


class Mmsg(models.Model):
    mmsg_code = models.CharField(max_length=10, blank=True, null=True)
    msg_date_time = models.DateTimeField(blank=True, null=True)
    chapter = models.CharField(max_length=3, blank=True, null=True)
    section = models.CharField(max_length=3, blank=True, null=True)
    equip_number = models.CharField(max_length=20, blank=True, null=True)
    fault_report = models.ForeignKey(
        FaultReport, on_delete=models.CASCADE, related_name='plf')

    fde = models.ForeignKey(
        Fde, on_delete=models.CASCADE, related_name='mmsgs', null=True, blank=True)

    defect_status = models.CharField(max_length=10, blank=True, null=True)
    defect_ref = models.CharField(max_length=20, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'mmsg'


# class FdeMmsg(models.Model):
#     plf = models.ForeignKey(FaultReport, models.CASCADE, related_name='plf')
#     fde = models.ForeignKey(Fde, models.CASCADE,
#                             blank=True, null=True, related_name='fde')
#     mmsg = models.ForeignKey(Mmsg, models.CASCADE,
#                              blank=True, null=True, related_name='mmsg')

#     class Meta:
#         db_table = 'fde_mmsg'


class Plane(models.Model):
    tail = models.CharField(max_length=10)
    airline = models.ForeignKey(
        Airline, on_delete=models.CASCADE, related_name='planes')
    type = models.ForeignKey(
        'PlaneType', on_delete=models.CASCADE, related_name='planes')

    class Meta:
        db_table = 'plane'


class PlaneType(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        db_table = 'plane_type'


class Snapshot(models.Model):
    type = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    arriving = models.CharField(max_length=9, blank=True, null=True)
    departing = models.CharField(max_length=9, blank=True, null=True)
    flight = models.CharField(max_length=9, blank=True, null=True)
    phase = models.CharField(max_length=9, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    plane = models.ForeignKey(
        Plane, on_delete=models.CASCADE, related_name='snaphots', blank=True, null=True)
    raw = models.ForeignKey(AcarsMsgRaw, on_delete=models.DO_NOTHING,
                            related_name='snaphots', blank=True, null=True)

    class Meta:
        db_table = 'snapshot'


class User(models.Model):
    username = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=128)
    airline = models.ForeignKey(Airline, models.DO_NOTHING)
    role = models.ForeignKey('UserRole', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user'


class UserRole(models.Model):
    role = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'user_role'
