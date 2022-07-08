from datetime import datetime
from hashlib import new

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, DeleteView, CreateView, UpdateView

from .models import *


from .forms import *
from . import services

@method_decorator(login_required, name='dispatch')
class OccurrencesDetailsView(ListView):
    template_name = 'occurrences_details.html'

    def get_queryset(self):
        return services.get_occurrences_details_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tail'] = self.request.GET['tail']
        context['ata_chapter'] = self.request.GET['ataChapter']
        context['from_date'] = datetime.strptime(
            self.request.GET['fromDate'], '%Y-%m-%d')
        context['to_date'] = datetime.strptime(
            self.request.GET['toDate'], '%Y-%m-%d')
        return context


@method_decorator(login_required, name='dispatch')
class OccurrencesView(View):
    form_class = OccurrencesDataRangeForm
    template_name = 'occurrences.html'
    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, 'occurrences.html', context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            occurrences_table = services.get_occurrences_df(
                form.cleaned_data, request)
            context['occurrences_table'] = occurrences_table
        return render(request, 'occurrences.html', context=context)

@method_decorator(login_required, name='dispatch')
class OpenDefectView(CreateView):
    model = Defect
    template_name = 'defect_form.html'
    form_class = CreateDefectForm
    success_url = reverse_lazy('defects')

    def form_valid(self, form):     
        self.defect = form.save(commit=False)
        services.open_defect(self.defect, self.kwargs.get('pk'))
        return super().form_valid(form)
  

@method_decorator(login_required, name='dispatch')
class DefectsView(ListView):
    template_name = 'defect_list.html'
    model = Defect

 


@method_decorator(login_required, name='dispatch')
class EditDefectView(UpdateView):
    model = Defect
    success_url = reverse_lazy('defects')
    template_name = 'defect_form.html'
    form_class = EditDefectForm

    def form_valid(self, form):
        old_defect = self.get_object()     
        new_defect = form.save()
        services.add_defect_to_history(new_defect, old_defect.status, new_defect.status, new_defect.action)
        return super().form_valid(form)


        
