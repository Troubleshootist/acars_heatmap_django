from . import views
from django.urls import path


urlpatterns = [
    path('occurrences', views.OccurrencesView.as_view(), name='occurrences'),
    path('occurrences/details/', views.OccurrencesDetailsView.as_view(),
         name='occurrences_details_1'),
    path('occurrences/details/<pk>/open_defect', views.OpenDefectView.as_view(), name='open_defect'),
    path('defects', views.DefectsView.as_view(), name='defects'),
    path('defect/<pk>/edit_defect', views.EditDefectView.as_view(), name='edit_defect'),
]
