import pandas as pd
import numpy as np
from datetime import datetime
from .models import *


def get_occurrences_df(data_from_form, request):
    """Returns the occurrences for the given data (start, end date)"""
    occurrences = Mmsg.objects.filter(
        msg_date_time__gte=data_from_form['from_date'],
        msg_date_time__lte=data_from_form['to_date'],
        fault_report__raw__plane__airline_group__in=request.user.groups.all()
    )
    df = pd.DataFrame(occurrences.values(
        'mmsg_code', 'chapter', 'fault_report__raw__plane__tail'))
    try:
        pivot = pd.pivot_table(df, columns='fault_report__raw__plane__tail',
                               aggfunc='count',
                               fill_value=0,
                               margins=True,
                               index=['chapter']).sort_values(by='All', ascending=False, axis=1)
    except:
        pivot = pd.DataFrame()

    return pivot.to_html(
        classes='table table-bordered table-hover table-sm', table_id='occurrences_table')


def get_occurrences_details_dataset(request):
    tail = request.GET['tail']
    ata_chapter = request.GET['ataChapter']
    from_date = datetime.strptime(request.GET['fromDate'], '%Y-%m-%d')
    to_date = datetime.strptime(request.GET['toDate'], '%Y-%m-%d')

    messages = Mmsg.objects.filter(chapter=ata_chapter,
                                   fault_report__raw__plane__tail=tail,
                                   msg_date_time__gte=from_date,
                                   msg_date_time__lte=to_date,
                                   fault_report__raw__plane__airline_group__in=request.user.groups.all())

    return messages.values('mmsg_code',
                           'fde__fde_code',
                           'msg_date_time',
                           'equip_number',
                           'fault_report__departing',
                           'fault_report__arriving',
                           'fault_report__flight',
                           'defect_status',
                           'defect_ref'
                           )


def get_occurrences_details_queryset(request):
    tail = request.GET['tail']
    ata_chapter = request.GET['ataChapter']
    from_date = datetime.strptime(request.GET['fromDate'], '%Y-%m-%d')
    to_date = datetime.strptime(request.GET['toDate'], '%Y-%m-%d')

    messages = Mmsg.objects.filter(chapter=ata_chapter,
                                   fault_report__raw__plane__tail=tail,
                                   msg_date_time__gte=from_date,
                                   msg_date_time__lte=to_date,
                                   fault_report__raw__plane__airline_group__in=request.user.groups.all())
    return messages
