import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "predictive_maint.settings")

import django
from msgs.models import *
django.setup()

from django.core.management import call_command

import re
from datetime import datetime


raw_messages = AcarsMsgRaw.objects.filter(processed = 0, type='FH')
count_processed = 0
for raw_message in raw_messages:
    text = raw_message.text
    plf_message = FaultReport()
       
    raw_date = re.findall(r'DATE:\s(\d{2}\w{3}\d{2})', text)[0]
    raw_time = re.findall(r'TIME:\s(\d{4})', text)[0]
    plf_message.report_datetime = datetime.strptime(raw_date+raw_time, '%d%b%y%H%M')
    plf_message.raw = raw_message
    plf_message.save()
    
    mmsgs_info = re.findall(
        r'(?=Maintenance Message:).+?(?=Maintenance Message:)', text)
    try:
        last_mmsg_info = re.findall(
            r'Maintenance Message: (?!.*Maintenance Message: )(.+)', text)[0]
        mmsgs_info.append(last_mmsg_info)
    except IndexError:
        print('no last')

    for mmsg_raw in mmsgs_info:

        maint_message_code = re.search(r'\d{2}-\d{5}', mmsg_raw)[0]
        chapter = maint_message_code[:2]
        legs_info = re.findall(r'(?=Leg).+?(?=Leg)', mmsg_raw)
        last_leg = re.findall(r'Leg(?!.*Leg)(.+)', mmsg_raw)[0]
        legs_info.append(last_leg)
        for leg_raw in legs_info:
            print(leg_raw)
            mmsg = Mmsg()
            mmsg.chapter = chapter
            mmsg.defect_status = 'Not open'
            mmsg.mmsg_code = maint_message_code
            raw_date_time = re.findall(
                r'Occurred at (\d{4})z (\d{2}\w{3}\d{2})', leg_raw)
            raw_time = raw_date_time[0][0]
            raw_date = raw_date_time[0][1]
            mmsg.msg_date_time = datetime.strptime(
                raw_date+raw_time, '%d%b%y%H%M')
            mmsg.note = leg_raw
            mmsg.fault_report = plf_message

            try:
                fde_code = re.findall(r'Fault Code: (\d{3}\s\d{3}\s\d{2})', leg_raw)[0]
                fde = Fde()
                fde.fde_code = fde_code.replace(' ', '')
                fde.fault_report = plf_message
                fde.save()
                mmsg.fde = fde
            except IndexError:
                print('non-FDE')

            repeat = Mmsg.objects.filter(mmsg_code=mmsg.mmsg_code, msg_date_time=mmsg.msg_date_time)
            if repeat.exists():
                print('Not saved, repeated: ', mmsg)
                # pass
            else:
                mmsg.save()
                print('Saved: ', mmsg)
                # pass

    





