import pandas as pd
import numpy as np
from datetime import datetime
from .models import *



def get_occurrences_df(data_from_form, request):
    """Returns the occurrences for the given data (start, end date)"""
    occurrences = Mmsg.objects.filter(
        msg_date_time__gte=data_from_form['from_date'],
        msg_date_time__lte=data_from_form['to_date'],
        fault_report__raw__plane__airline_group__in=request.user.groups.all(),
        defect__status__in=data_from_form['status']
    )
    df = pd.DataFrame(occurrences.values(
        'mmsg_code', 'chapter', 'fault_report__raw__plane__tail'))
    df = df.rename(columns={"mmsg_code": "MMSGs count",
                            "chapter": "ATA",
                            "fault_report__raw__plane__tail": 'A/C Reg.'})
    try:
        pivot = pd.pivot_table(df, columns='A/C Reg.',
                               aggfunc='count',
                               fill_value=0,
                               margins=True,
                               index=['ATA'])
        pivot = pivot.iloc[:, :-1]

    except:
        pivot = pd.DataFrame()

    return pivot.to_html(
        classes='table table-bordered table-hover table-sm',
        table_id='occurrences_table')


def get_occurrences_details_queryset(request):
    tail = request.GET['tail']
    plane = Plane.objects.get(tail=tail)
    ata_chapter = request.GET['ataChapter']
    from_date = datetime.strptime(request.GET['fromDate'], '%Y-%m-%d')
    to_date = datetime.strptime(request.GET['toDate'], '%Y-%m-%d')
    if ata_chapter == 'All':
        messages = Mmsg.objects.filter(fault_report__raw__plane__tail=tail,
                                       msg_date_time__gte=from_date,
                                       msg_date_time__lte=to_date,
                                       fault_report__raw__plane__airline_group__in=request.user.groups.all())
        history_messages = Mmsg.objects.filter(fault_report__raw__plane__tail=tail,
                                               msg_date_time__lt=from_date,
                                               fault_report__raw__plane__airline_group__in=request.user.groups.all())
    else:
        messages = Mmsg.objects.filter(chapter=ata_chapter,
                                       fault_report__raw__plane__tail=tail,
                                       msg_date_time__gte=from_date,
                                       msg_date_time__lte=to_date,
                                       fault_report__raw__plane__airline_group__in=request.user.groups.all())
        history_messages = Mmsg.objects.filter(chapter=ata_chapter,
                                               fault_report__raw__plane__tail=tail,
                                               msg_date_time__lt=from_date,
                                               fault_report__raw__plane__airline_group__in=request.user.groups.all())

    queryset = {'messages': messages,
                'history_messages': history_messages}
    return queryset


