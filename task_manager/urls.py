from django.urls import path
from task_manager import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_tasks, name='project_tasks'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/tasks/create/', views.task_create, name='task_create'),
    path('projects/<int:project_id>/tasks/', views.task_list, name='task_list'),
]
