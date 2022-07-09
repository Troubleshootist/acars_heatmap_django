from django.db import models

class TaskCard(models.Model):
    class Meta:
        db_table = 'task_card'
    number = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    ata_chapter = models.CharField(max_length=20)
    plane_type = models.ForeignKey('msgs.PlaneType', on_delete=models.DO_NOTHING, blank=True, null=True)
    defect = models.ForeignKey(Defect, on_delete=models.DO_NOTHING, related_name='task_card', blank=True, null=True)


class TaskCardStep(models.Model):
    class Meta:
        db_table = 'task_card_step'
    number = models.IntegerField()
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    task_card = models.ForeignKey(TaskCard, on_delete=models.CASCADE, related_name='steps')

class Materials(models.Model):
    class Meta:
        db_table = 'task_card_material'
    part_number = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    qty = models.CharField(max_length=10)
    task_card = models.ForeignKey(TaskCard, on_delete=models.CASCADE, related_name='materials')
