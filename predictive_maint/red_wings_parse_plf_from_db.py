import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "predictive_maint.settings")

import django
django.setup()

from django.core.management import call_command

import re
from datetime import datetime

from msgs.models import *

raw_messages = AcarsMsgRaw.objects.filter(processed = 0, type='PLF')
count_processed = 0
for raw_message in raw_messages:
    text = raw_message.text
    plf_message = FaultReport()
    
    
    flight = re.search(r'RWZ\d+', text)
    if flight:
        plf_message.flight = flight[0]

    depart_arrive_info = re.findall(r'([A-Z]{4})/([A-Z]{4})', text)
    if len(depart_arrive_info) > 0:
        plf_message.departing = depart_arrive_info[0][0]
        plf_message.arriving = depart_arrive_info[0][1]

    raw_date = re.findall(r'DATE:\s(\d{2}\w{3}\d{2})', text)[0]
    raw_time = re.findall(r'TIME:\s(\d{4})', text)[0]
    plf_message.report_datetime = datetime.strptime(raw_date+raw_time, '%d%b%y%H%M')
    plf_message.raw = raw_message
    plf_message.save()
    
    fde_info = re.findall(r'(?<=FDE: ).+?(?=FDE)', text)
    last_fde_info = re.search(r'FDE(?!.*FDE)(.+)(?=-------)', text)
    if last_fde_info:
        fde_info.append(last_fde_info[0])

    for fde_record in fde_info:
        fde = Fde()
        raw_fde_code = re.findall(r'Fault Code: ([0-9 ]{10})', fde_record)[0]
        fde.fde_code = raw_fde_code.replace(' ','')
        fde.fault_report = plf_message
        fde.save()
        plf_message.fde_messages.add(fde)


        mmsgs_info = re.findall(r'(?=Message: ).+?(?=\[)', f'{fde_record}[]')
        for mmsg_record in mmsgs_info:
            mmsg = Mmsg()
            
            mmsg.mmsg_code = re.findall(r'Message: (\d{2}-\d{5})', mmsg_record)[0]
            mmsg.chapter = mmsg.mmsg_code[:2]

            raw_time = re.findall(r'Occurred at (\d{4})z\s(\d{2}\w{3}\d{2})', mmsg_record)[0][0]
            raw_date = re.findall(r'Occurred at (\d{4})z\s(\d{2}\w{3}\d{2})', mmsg_record)[0][1]
            mmsg.msg_date_time = datetime.strptime(raw_date+raw_time, '%d%b%y%H%M')
            mmsg.note = mmsg_record
            mmsg.defect_status = 'Not open'
            mmsg.fault_report = plf_message
            mmsg.fde = fde
            
            repeat = Mmsg.objects.filter(mmsg_code=mmsg.mmsg_code, msg_date_time=mmsg.msg_date_time)
            if repeat.exists():
                print('Not saved, repeated: ', mmsg)
            else:
                mmsg.save()
                print('Saved: ', mmsg)
            
    

    non_correlated_text = re.findall(r'(?=which).+', text)

    nc_mmsgs_info = re.findall(r'(?=Message: ).+?(?=\[)', f'{non_correlated_text}[]')
    for mmsg_record in nc_mmsgs_info:
        mmsg = Mmsg()
        
        mmsg.mmsg_code = re.findall(r'Message: (\d{2}-\d{5})', mmsg_record)[0]
        mmsg.chapter = mmsg.mmsg_code[:2]

        raw_time = re.findall(r'Occurred at (\d{4})z\s(\d{2}\w{3}\d{2})', mmsg_record)[0][0]
        raw_date = re.findall(r'Occurred at (\d{4})z\s(\d{2}\w{3}\d{2})', mmsg_record)[0][1]
        mmsg.msg_date_time = datetime.strptime(raw_date+raw_time, '%d%b%y%H%M')
        mmsg.note = mmsg_record
        mmsg.defect_status = 'Not open'
        mmsg.fault_report = plf_message
        repeat = Mmsg.objects.filter(mmsg_code=mmsg.mmsg_code, msg_date_time=mmsg.msg_date_time)
        if repeat.exists():
            print('Not saved, repeated: ', mmsg)
        else:
            mmsg.save()
            print('Saved: ', mmsg)





