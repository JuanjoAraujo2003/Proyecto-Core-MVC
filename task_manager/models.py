from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from abc import ABC, abstractmethod
# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=True)
    ROLES = (
        ('designer', 'Diseñador'),
        ('frontend', 'Frontend Developer'),
        ('backend', 'Backend Developer'),
        ('qa', 'QA Engineer'),
    )
    role = models.CharField(max_length=50, choices=ROLES, default='frontend')

    def __str__(self):
        return self.username

class Project(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField(default=date.today, verbose_name="End Date")
    created_by = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='created_projects'
    )


    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="Project"
    )
    title = models.CharField(max_length=100, verbose_name="Task Title")
    description = models.TextField(verbose_name="Task Description")
    assigned_to = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
        verbose_name="Assigned To"
    )
    start_date = models.DateField(default=date.today,verbose_name="Start Date")
    end_date = models.DateField(default=date.today, verbose_name="End Date")
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='low',
        verbose_name="Priority"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Status"
    )

    estimated_hours = models.IntegerField(default=1)
    required_role = models.CharField(max_length=50, default='frontend', choices=User.ROLES)

    def __str__(self):
        return f"{self.title} ({self.status})"

## Singleton
class AppConfigSingleton(models.Model):
    site_name = models.CharField(max_length=255, default="Task Manager")
    maintenance_mode = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.pk = 1  # Garantiza que siempre haya una única instancia
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        return cls.objects.get_or_create(pk=1)[0]  # Devuelve siempre la misma instancia

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuración"

    def __str__(self):
        return f"{self.site_name} - {'Maintenance Mode' if self.maintenance_mode else 'Running'}"

# Patrón Strategy para asignación de tareas
class TaskAssignmentStrategy(ABC):
    @abstractmethod
    def assign_task(self, task):
        pass

# Asignar al trabajador con menos tareas
class AssignToLeastBusyWorker(TaskAssignmentStrategy):
    def assign_task(self, task):
        workers = User.objects.filter(is_worker=True).annotate(task_count=models.Count('tasks')).order_by('task_count')
        if workers.exists():
            task.assigned_to = workers.first()
            task.status = 'in_progress'
            task.save()

# Asignar según la prioridad de la tarea
class AssignByTaskPriority(TaskAssignmentStrategy):
    def assign_task(self, task):
        workers = User.objects.filter(is_worker=True, role=task.required_role).order_by('tasks__priority')
        if workers.exists():
            task.assigned_to = workers.last()  # El trabajador con menos tareas de alta prioridad
            task.status = 'in_progress'
            task.save()

# Contexto del Strategy
class TaskAssignmentContext:
    def __init__(self, strategy: TaskAssignmentStrategy):
        self.strategy = strategy

    def execute_assignment(self, task):
        self.strategy.assign_task(task)