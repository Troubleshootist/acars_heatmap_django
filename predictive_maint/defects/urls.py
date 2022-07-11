from django.urls import path


from . import views

urlpatterns = [
    path('defect_list', views.DefectsView.as_view(), name='defect_list'),
    path('defect_list/create', views.OpenDefectFromScratch.as_view(), name='open_defect'),
    path('defect/<pk>/edit_defect', views.EditDefectView.as_view(), name='edit_defect'),
    path('occurrences/details/<pk>/open_defect', views.OpenDefectByMessageView.as_view(), name='open_defect'),
]

