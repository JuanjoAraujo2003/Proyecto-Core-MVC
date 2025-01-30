from django.urls import path, include
from task_manager import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)


urlpatterns = [
    path('', views.project_list , name='project_list'),
    path('projects/<int:project_id>/', views.project_tasks, name='project_tasks'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/tasks/create/', views.task_create, name='task_create'),
    path('projects/<int:project_id>/tasks/', views.task_list, name='task_list'),
    path('projects/<int:project_id>/tasks/<int:task_id>/edit/', views.edit_task, name='task_edit'),
    path('projects/<int:project_id>/tasks/<int:task_id>', views.delete_task, name='task_delete'),
    path('employees/create/', views.create_employee, name='create_employee'),
    path('employees/', views.list_employees, name='list_employees'),
    path('employees/<int:employee_id>/', views.delete_employees, name='employee_delete'),
    path('employees/<int:employee_id>/edit/', views.edit_employee, name='employee_edit'),
    path('login/', views.login_view , name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('projects/<int:project_id>/optimize_tasks/', views.optimize_tasks, name='optimize_tasks'),
    path('api/', include(router.urls)),

]
