from datetime import datetime
from hashlib import new


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



        
