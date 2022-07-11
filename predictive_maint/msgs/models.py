from time import strftime

from django.contrib.auth.models import Group
from django.urls import reverse
from django.db import models


class AcarsMsgRaw(models.Model):
    filename = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    processed = models.IntegerField(blank=True, null=True)
    plane = models.ForeignKey(
        'Plane', on_delete=models.CASCADE, related_name='raw_messages')

    class Meta:
        db_table = 'acars_msg_raw'


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
    fim_ref = models.CharField(max_length=50, blank=True, null=True)
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

    defect_status = models.CharField(
        max_length=10, blank=True, null=True, default='Not open')
    defect_ref = models.CharField(max_length=20, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    defect = models.ForeignKey(
        'defects.Defect', on_delete=models.CASCADE, blank=True, null=True, related_name='messages')
    description = models.ForeignKey(
        MessageDescription, models.DO_NOTHING, blank=True, null=True, related_name='maint_message')

    class Meta:
        db_table = 'mmsg'
        ordering = ['-msg_date_time']

    def __str__(self):
        return f"{self.mmsg_code}, {self.msg_date_time.strftime('%d %b %Y, %H:%M')}"


class Plane(models.Model):
    tail = models.CharField(max_length=10)

    type = models.ForeignKey(
        'PlaneType', on_delete=models.CASCADE, related_name='planes')
    airline_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'plane'

    def __str__(self) -> str:
        return f'{self.tail}, {self.airline_group}'


class PlaneType(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        db_table = 'plane_type'

    def __str__(self):
        return f'{self.type}'

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
