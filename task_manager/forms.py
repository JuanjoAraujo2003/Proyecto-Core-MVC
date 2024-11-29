from django import forms
from .models import Project, Task, User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'end_date', 'priority']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'end_date' , 'priority', 'status', 'assigned_to', 'required_role']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']
        widgets = {
            'password': forms.PasswordInput()
        }

