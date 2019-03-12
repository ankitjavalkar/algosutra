from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'todo'
urlpatterns = [
    # path('login/', auth.views.login, {'template_name': 'login.html'}),#views.login, name='login'),
    # path('logout/', auth.views.logout, {'next_page': '/login/'}),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('tasks/', views.tasks, name='tasks'),
    path('task/', views.task_detail, name='add_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),

    path('categories/', views.categories, name='categories'),
    path('category/', views.category_detail, name='add_category'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),

    path('tasklists/', views.task_lists, name='task_lists'),
    path('tasklist/', views.task_list_detail, name='add_task_list'),
    path('tasklist/<int:task_list_id>/detail', views.task_list_detail, name='task_list_detail'),
]
