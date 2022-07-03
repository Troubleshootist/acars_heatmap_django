import os
from pydoc import describe
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "predictive_maint.settings")

import django
django.setup()

from django.core.management import call_command

import re
from datetime import datetime
from msgs.models import *


import pandas as pd
filepath = 'local/ATA 26 notrifications.xlsx'
ATA = '26'
PLANE_TYPE_ID = 4  
plane_type = PlaneType.objects.get(pk=PLANE_TYPE_ID)
df = pd.read_excel(filepath)
message_descriptions = []
for column, row in df.iterrows():
    repeat = MessageDescription.objects.filter(plane_type=plane_type, 
                                               mmsg=row['mmsg_code'], 
                                               description=row['mmsg_description'],
                                               major_notification_name=row['major_notification_name'])
    if not repeat.exists():
        message_description = MessageDescription()
        message_description.mmsg = row['mmsg_code']
        message_description.ata = ATA
        message_description.description = row['mmsg_description']
        message_description.major_notification_name = row['major_notification_name']
        message_description.minor_notification_name = row['minor_notification_name']
        message_description.fim_ref = row['FIM ref.']
        message_description.plane_type = plane_type
        message_descriptions.append(message_description)

        message_description.save()
        messages_in_base = Mmsg.objects.filter(fault_report__raw__plane__type = plane_type, mmsg_code = message_description.mmsg).update(description=message_description)

# MessageDescription.objects.bulk_create(message_descriptions)
print(len(message_descriptions))