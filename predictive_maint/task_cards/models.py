
from django.db import models


class TaskCard(models.Model):
    class Meta:
        db_table = 'task_card'
    number = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    ata_chapter = models.CharField(max_length=20, blank=True, null=True)
    issued_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    plane_type = models.ForeignKey('msgs.PlaneType', on_delete=models.DO_NOTHING, blank=True, null=True)
    defect = models.ForeignKey('defects.Defect', on_delete=models.DO_NOTHING, related_name='task_card', blank=True, null=True)

    def __str__(self):
        return f'{self.number} - {self.description}'
    


class TaskCardStep(models.Model):
    class Meta:
        db_table = 'task_card_step'
        ordering = ['number']
    number = models.IntegerField(blank=True, null=True)
    text = models.TextField(default="-----")
    image = models.ImageField(upload_to=f'images/%Y/%m/%d/%H/%M', null=True, blank=True)
    task_card = models.ForeignKey(TaskCard, on_delete=models.CASCADE, related_name='steps')

    
class TaskCardMaterial(models.Model):
    class Meta:
        db_table = 'task_card_material'
    part_number = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    qty = models.CharField(max_length=10)
    task_card = models.ForeignKey(TaskCard, on_delete=models.CASCADE, related_name='materials')
