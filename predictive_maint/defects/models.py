from asyncio.base_tasks import _task_get_stack
from django.db import models
from pandas import describe_option


class Defect(models.Model):

    plane = models.ForeignKey(
        'msgs.Plane', on_delete=models.CASCADE, related_name='defects', null=True, blank=True)
    reference = models.CharField(max_length=20)
    description = models.CharField(max_length=255, null=True, blank=True)
    action = models.CharField(max_length=255, null=True, blank=True)

    status = models.ForeignKey(
        'DefectStatus', on_delete=models.CASCADE, related_name="defects")

    def __str__(self):
        return f'{self.plane}, {self.reference}, {self.description}'
    

    class Meta:
        db_table = 'defect'
        ordering = ['-id']


class DefectStatus(models.Model):
    condition = models.CharField(max_length=20)

    def __str__(self):
        return self.condition

    class Meta:
        db_table = 'defect_status'


class DefectHistory(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    before_status = models.ForeignKey(
        DefectStatus, on_delete=models.CASCADE, related_name='before_history')
    after_status = models.ForeignKey(
        DefectStatus, on_delete=models.CASCADE, related_name='after_history')
    defect = models.ForeignKey(
        Defect, on_delete=models.CASCADE, related_name="history")
    action = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'defect_history'



    