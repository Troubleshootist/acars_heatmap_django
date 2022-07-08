from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy

from msgs.models import *
from .forms import *
from . import services


class OpenDefect(CreateView):
    model: Defect
    template_name = 'defect_form.html'
    success_url = reverse_lazy('defect_list')

    def form_valid(self, form):
        self.defect = form.save(commit=False)
        services.open_defect_by_message(self.defect, self.kwargs.get('pk'))
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class OpenDefectFromScratch(OpenDefect):
    form_class = CreateDefect


@method_decorator(login_required, name='dispatch')
class OpenDefectByMessageView(OpenDefect):
    form_class = CreateDefectByMessageForm


@method_decorator(login_required, name='dispatch')
class DefectsView(ListView):
    template_name = 'defect_list.html'
    model = Defect

    def get_queryset(self):
        return services.get_defect_by_user_permission(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class EditDefectView(UpdateView):
    model = Defect
    success_url = reverse_lazy('defect_list')
    template_name = 'defect_form.html'
    form_class = EditDefectForm

    def form_valid(self, form):
        old_defect = self.get_object()
        new_defect = form.save()
        services.add_defect_to_history(
            new_defect, old_defect.status, new_defect.status, new_defect.action)
        return super().form_valid(form)
