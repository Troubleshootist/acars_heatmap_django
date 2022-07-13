
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from extra_views import CreateWithInlinesView, InlineFormSetFactory

from .models import *
from .forms import *


@method_decorator(login_required, name='dispatch')
class CreateTaskCardView(CreateView):
    model = TaskCard
    template_name = 'create_task_card.html'
    form_class = CreateTaskCardForm
    success_url = reverse_lazy('task_card_list')

    def get_context_data(self, **kwargs):
        context = super(CreateTaskCardView, self).get_context_data(**kwargs)
        context['steps_formset'] = StepsFormSet()
        context['materials_formset'] = MaterialsFormSet()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        task_card_steps_form = StepsFormSet(
            self.request.POST, self.request.FILES)
        task_card_materials_form = MaterialsFormSet(self.request.POST)
        if form.is_valid() and task_card_steps_form.is_valid() and task_card_materials_form.is_valid():
            return self.form_valid(form, task_card_steps_form, task_card_materials_form)
        else:
            return self.form_invalid(form, task_card_steps_form, task_card_materials_form)

    def form_valid(self, form, task_card_steps_form, task_card_materials_form):
        self.task_card = form.save()

        for step in task_card_steps_form.save(commit=False):
            step.task_card = self.task_card
            step.save()
        for material in task_card_materials_form.save(commit=False):
            material.task_card = self.task_card
            material.save()
        return super().form_valid(form)

    def form_invalid(self, form, task_card_steps_form, task_card_materials_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.

        """
        return self.render_to_response(
            self.get_context_data(steps_formset=task_card_steps_form,
                                  materials_formset=task_card_materials_form))


@method_decorator(login_required, name='dispatch')
class TaskCardUpdateView(UpdateView):
    model = TaskCard
    template_name = 'create_task_card.html'
    form_class = CreateTaskCardForm
    success_url = reverse_lazy('task_card_list')

    def get_context_data(self, **kwargs):
        context = super(TaskCardUpdateView, self).get_context_data(**kwargs)
        preloaded_steps_formset = StepsFormSet()
        preloaded_steps_formset.queryset = self.get_object().steps.all()
        context['steps_formset'] = preloaded_steps_formset

        preloaded_materials_formset = MaterialsFormSet()
        preloaded_materials_formset.queryset = self.get_object().materials.all()
        context['materials_formset'] = preloaded_materials_formset

        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        task_card_steps_form = StepsFormSet(
            self.request.POST, self.request.FILES, instance=self.get_object())
        task_card_materials_form = MaterialsFormSet(self.request.POST, instance=self.get_object())
        if form.is_valid() and task_card_steps_form.is_valid() and task_card_materials_form.is_valid():
            return self.form_valid(form, task_card_steps_form, task_card_materials_form)
        else:
            return self.form_invalid(form, task_card_steps_form, task_card_materials_form)

    def form_valid(self, form, task_card_steps_form, task_card_materials_form):


        for step in task_card_steps_form.save(commit=False):
            step.task_card = self.get_object()
            step.save()
        for material in task_card_materials_form.save(commit=False):
            material.task_card = self.get_object()
            material.save()
        return super().form_valid(form)

    def form_invalid(self, form, task_card_steps_form, task_card_materials_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.

        """
        return self.render_to_response(
            self.get_context_data(steps_formset=task_card_steps_form,
                                  materials_formset=task_card_materials_form))


@method_decorator(login_required, name='dispatch')
class TaskCardsListView(ListView):
    model = TaskCard
    template_name = 'task_card_list.html'


@method_decorator(login_required, name='dispatch')
class TaskCardDetailView(DetailView):
    model = TaskCard
    template_name = 'task_card_detail.html'


class TaskCardStepInline(InlineFormSetFactory):
    model = TaskCardStep
    fields = '__all__'
    factory_kwargs = {'extra': 6}


class MaterialsInline(InlineFormSetFactory):
    model = TaskCardMaterial
    fields = '__all__'


@method_decorator(login_required, name='dispatch')
class CreateTaskCardViewaaaaa(CreateWithInlinesView):
    model = TaskCard
    inlines = [TaskCardStepInline, MaterialsInline]
    fields = '__all__'
    template_name = 'create_task_card.html'
    factory_kwargs = {'extra': 6}
