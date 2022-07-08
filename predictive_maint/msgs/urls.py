from . import views
from django.urls import path


urlpatterns = [
    path('occurrences', views.OccurrencesView.as_view(), name='occurrences'),
    path('occurrences/details/', views.OccurrencesDetailsView.as_view(),
         name='occurrences_details_1'),

]
