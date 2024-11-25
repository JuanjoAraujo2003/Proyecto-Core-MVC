from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task, User
from .forms import ProjectForm, TaskForm, EmployeeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Create your views here.

@login_required
def project_list(request):
    if request.user.is_admin:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(tasks__assigned_to=request.user).distinct()
    return render(request, 'project_list.html', {'projects': projects})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})

def project_tasks(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)  # Recupera las tareas asociadas al proyecto
    return render(request, 'project_tasks.html', {'project': project, 'tasks': tasks})

def task_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    return render(request, 'task_list.html', {'project': project, 'tasks': tasks})

def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('task_list', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'project': project})

def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_worker = True
            user.save()
            return redirect('list_employees')
    else:
        form = EmployeeForm()
    return render(request, 'employees.html', {'form': form})

def list_employees(request):
    employees = User.objects.filter(is_worker=True)
    return render(request, 'employees_list.html', {'employees': employees})

def delete_employees(request, employee_id):
    employees = User.objects.filter(is_worker=True, id=employee_id)
    employees.delete()
    return redirect('list_employees')

def edit_employee(request, employee_id):
    employee = get_object_or_404(User, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('list_employees')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form})