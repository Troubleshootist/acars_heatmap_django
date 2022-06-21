from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import OccurrencesDataRangeForm
from . import services

# Create your views here.

def index(request):
    context = {'greetings': 'Hello, world!'}
    return render(request, 'index.html', context=context)

def occurrences(request):
    context = {}
    if request.method == 'POST':
        form = OccurrencesDataRangeForm(request.POST)
        if form.is_valid():
            occurrences_table = services.get_occurrences_df(form.cleaned_data)
            context['occurrences_table'] = occurrences_table
    else:
        form = OccurrencesDataRangeForm()
    context['form'] = form
    return render(request, 'occurrences.html', context=context)

def occurrences_details(request):
    occurrences_details_dataset = services.get_occurrences_details_dataset(request)
    return JsonResponse(occurrences_details_dataset)
