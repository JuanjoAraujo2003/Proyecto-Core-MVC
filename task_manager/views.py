from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task, User
from .forms import ProjectForm, TaskForm, EmployeeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
@csrf_exempt
def project_list(request):
    if request.user.is_admin:
        print("Usuario administrador")
        projects = Project.objects.all()
        if not projects.exists():
            # Si no hay proyectos, renderiza una página con un mensaje
            return render(request, 'project_list.html', {'projects': None, 'message': 'No hay proyectos registrados.'})
        total_tasks, completed_tasks = project_progress(projects.first().id)
        return render(request, 'project_list.html', {'projects': projects, 'total_tasks': total_tasks, 'completed_tasks': completed_tasks})
    else:
        print("Usuario empleado")
        # Filtra los proyectos con tareas asignadas al usuario
        projects = Project.objects.filter(tasks__assigned_to=request.user).distinct()

        if projects.exists():
            # Redirige al primer proyecto asignado
            project_id = projects.first().id
            return redirect('project_tasks', project_id=project_id)
        else:
            # Si no hay proyectos, muestra un mensaje
            return render(request, 'project_tasks.html', {'projects': None, 'tasks': None, 'message': 'No hay tareas asignadas a ti'})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            projects  = form.save(commit=False)
            projects.created_by = request.user
            projects.save()
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
    return render(request, 'project_tasks.html', {'project': project, 'tasks': tasks})

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
            user.set_password(form.cleaned_data['password'])
            user.is_worker = True
            user.save()
            return redirect('list_employees')
    else:
        form = EmployeeForm()
    return render(request, 'employees_form.html', {'form': form})

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
            emp = form.save()
            emp.set_password(form.cleaned_data['password'])
            return redirect('list_employees')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form})

def delete_task(request, project_id , task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list', project_id=task.project.id)

def edit_task(request, project_id ,task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'project_id': task.project.id})

def register(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_worker = True
            user.save()
            return redirect('login')
        else:
            print("Formulario invalido")
    else:
        form = EmployeeForm()
    return render(request, 'register.html', {'form': form})

def login_view (request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_admin:
                return redirect('project_list')
            elif user.is_worker:
                projects = Project.objects.filter(tasks__assigned_to=user).distinct()
                if projects.exists():
                    return redirect('project_tasks', project_id=projects.first().id)
                else:
                    return redirect('project_list')
        else:
            print("Formulario invalido")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def project_progress(project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    completed_tasks = tasks.filter(status='completed').count()
    total_tasks = tasks.count()
    if total_tasks == 0:
        progress = 0
    else:
        progress = (completed_tasks / total_tasks) * 100

    return total_tasks, completed_tasks

def optimize_tasks(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    pending_tasks = project.tasks.filter(status='pending')

    workers = User.objects.filter(is_worker=True).distinct()
    if not workers.exists():
        return render(request, 'optimize_tasks.html', {'project': project, 'message': 'No hay empleados disponibles'})

    worker_load = {
        worker: worker.tasks.filter(status='in_progress').count() for worker in workers
    }

    resigned_tasks = []
    unnasigned_tasks = []
    for task in pending_tasks:
        if not task.required_role:
            unnasigned_tasks.append(task)
            continue

        workers_with_role = [worker for worker in workers if worker.role == task.required_role]

        if not workers_with_role:
            unnasigned_tasks.append(task)
            continue
        less_loaded_worker = min(workers_with_role, key=lambda w: worker_load[w])

        task.assigned_to = less_loaded_worker

        task.status = 'in_progress'

        task.save()

        worker_load[less_loaded_worker] += 1

        resigned_tasks.append((task, less_loaded_worker))

    return render(request, 'optimize_task.html',
                  {'project': project, 'resigned_tasks': resigned_tasks, 'unnasigned_tasks': unnasigned_tasks})








