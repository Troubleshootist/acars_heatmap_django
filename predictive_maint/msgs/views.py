import re
import json
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View


from .forms import OccurrencesDataRangeForm
from . import services


@login_required
def index(request):
    context = {'greetings': 'Hello, world!'}
    return render(request, 'index.html', context=context)


@login_required
def occurrences(request):
    context = {}
    if request.method == 'POST':
        form = OccurrencesDataRangeForm(request.POST)
        if form.is_valid():
            occurrences_table = services.get_occurrences_df(
                form.cleaned_data, request)
            context['occurrences_table'] = occurrences_table
    else:
        form = OccurrencesDataRangeForm()
    context['form'] = form
    return render(request, 'occurrences.html', context=context)


@login_required
def occurrences_details(request):
    if request.method == 'GET':
        occurrences_details_dataset = services.get_occurrences_details_dataset(
            request)
        # return HttpResponse(response, content_type='application/json')
        serialized = json.dumps(
            list(occurrences_details_dataset), cls=DjangoJSONEncoder)
        return JsonResponse(serialized, safe=False)


@login_required
def occurrences_details_1(request):
    if request.method == 'POST':
        return render(request, 'occurrences_details.html')
    return render(request, 'occurrences_details.html')
