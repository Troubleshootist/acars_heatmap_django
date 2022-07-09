from . import views
from django.urls import path


urlpatterns = [
    path('create', views.OccurrencesView.as_view(), name='occurrences'),

]
