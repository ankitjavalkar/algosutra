from django.urls import path

from . import api_views

urlpatterns = [
    path('categories/', api_views.category_list),
    path('categories/<int:pk>/', api_views.category_detail),
    path('tasks/', api_views.task_list),
    path('tasks/<int:pk>/', api_views.task_detail),
    path('tasklists/', api_views.task_list_list),
    path('tasklists/<int:pk>/', api_views.task_list_detail),
]