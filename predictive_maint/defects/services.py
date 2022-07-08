from .models import *
from msgs.models import Mmsg
from datetime import datetime
import pytz


def open_defect_by_message(defect, message_id):
    # message_id приходит если открываем дефект по мессаджу. Если просто так открываем, то идем сразу к DefectHistory
    if message_id:
        message = Mmsg.objects.get(pk=message_id)
        plane = message.fault_report.raw.plane
        defect.plane = plane
        defect.status = DefectStatus.objects.get(condition='Open')
        defect.save()
        messages_to_open_defect = Mmsg.objects.filter(fault_report__raw__plane=plane,
                                                  mmsg_code = message.mmsg_code,
                                                  msg_date_time__gte=message.msg_date_time)
        messages_to_open_defect.update(defect=defect)
    else:
        defect.save()
    before_status = DefectStatus.objects.get(condition='Not Open')
    add_defect_to_history(defect, before_status, defect.status)


def add_defect_to_history(defect, before_status, after_status, action=None):
    defect_history = DefectHistory(
        defect=defect,
        date = datetime.now(tz=pytz.utc),
        before_status = before_status,
        after_status = after_status,
        action=action
    )
    defect_history.save()


def get_defect_by_user_permission(user):
    return Defect.objects.filter(plane__airline_group__in=user.groups.all())

