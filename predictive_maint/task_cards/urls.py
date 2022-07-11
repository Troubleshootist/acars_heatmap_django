from . import views
from django.urls import path


urlpatterns = [
    path('create', views.CreateTaskCardView.as_view(), name='task_card_create'),
    path('', views.TaskCardsListView.as_view(), name='task_card_list'),
    path('<pk>/update', views.TaskCardUpdateView.as_view(), name='task_card_update'),
    path('<pk>/details', views.TaskCardDetailView.as_view(), name='task_card_details'),

]
