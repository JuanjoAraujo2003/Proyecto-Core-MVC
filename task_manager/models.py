from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
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

    def __str__(self):
        return f"{self.title} ({self.status})"