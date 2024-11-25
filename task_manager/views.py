from django.shortcuts import render, get_object_or_404
from .models import Project, Task
from .forms import ProjectForm, TaskForm
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