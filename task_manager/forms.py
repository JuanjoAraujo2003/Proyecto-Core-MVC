from django import forms
from .models import Project, Task, User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'end_date']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'end_date' , 'priority', 'status', 'assigned_to']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'password': forms.PasswordInput()
        }