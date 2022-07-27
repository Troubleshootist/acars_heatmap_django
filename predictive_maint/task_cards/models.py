from operator import mod
from unicodedata import category
from django.core.exceptions import ValidationError


from django.db import models


def latex_sym_validator(string):
    restricted_chars = ['{', '}', '&']
    for char in string:
        if char in restricted_chars:
            raise ValidationError(
                message='%(string) contains restricted symbols',
                params={'value': string},
            )

class TaskCard(models.Model):
    class Meta:
        db_table = 'task_card'
    number = models.CharField(max_length=30, validators=[latex_sym_validator])
    description = models.CharField(max_length=255, validators=[latex_sym_validator])
    ata_chapter = models.CharField(max_length=20, blank=True, null=True, validators=[latex_sym_validator])
    issued_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    plane_type = models.ForeignKey('msgs.PlaneType', on_delete=models.DO_NOTHING, blank=True, null=True)
    defect = models.ForeignKey('defects.Defect', on_delete=models.DO_NOTHING, related_name='task_card', blank=True, null=True)

    def __str__(self):
        return f'{self.number} - {self.description}'
    


class TaskCardStep(models.Model):
    class Meta:
        db_table = 'task_card_step'

    text = models.TextField(default="", validators=[latex_sym_validator])
    image = models.ImageField(upload_to=f'images/%Y/%m/%d/%H/%M', null=True, blank=True)
    manhours = models.DecimalField(decimal_places=1, max_digits=3, default=0)
    
    staff_cat = models.ForeignKey('StaffCategory', on_delete=models.DO_NOTHING, blank=True, null=True)
    task_card = models.ForeignKey(TaskCard, on_delete=models.CASCADE, related_name='steps')

class StaffCategory(models.Model):
    class Meta:
        db_table = 'staff_category'

    category = models.CharField(max_length=5)
    
    def __str__(self) -> str:
        return self.category
    
class TaskCardMaterial(models.Model):
    class Meta:
        db_table = 'task_card_material'
    part_number = models.CharField(max_length=30, validators=[latex_sym_validator])
    description = models.CharField(max_length=50, validators=[latex_sym_validator])
    qty = models.CharField(max_length=10, validators=[latex_sym_validator])
    task_card = models.ForeignKey(TaskCard, on_delete=models.CASCADE, related_name='materials')
