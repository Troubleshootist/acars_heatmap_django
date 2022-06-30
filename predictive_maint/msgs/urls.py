from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('occurrences', views.occurrences, name='occurrences'),
    path('occurrences/ajax/details', views.occurrences_details,
         name='occurrences_details'),
    path('occurrences/details/', views.OccurrencesDetailsView.as_view(),
         name='occurrences_details_1')
]
