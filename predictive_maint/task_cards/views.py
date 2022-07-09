
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from .models import *

@method_decorator(login_required, name='dispatch')
class CreateTaskCard(CreateView):
    model = TaskCard
    template_name = 'create_task_card.html'