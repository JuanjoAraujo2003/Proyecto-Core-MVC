from rest_framework import serializers
from .models import User, Project, Task

# Serializer para el modelo User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_admin', 'is_worker', 'role',
            'first_name', 'last_name', 'date_joined'
        ]

# Serializer básico para el modelo Project
class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # Serializa el usuario que creó el proyecto
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Serializa las tareas relacionadas

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'priority', 'created_at', 'end_date',
            'created_by', 'tasks'
        ]

# Serializer básico para el modelo Task
class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())  # Relación con Project
    assigned_to = UserSerializer(read_only=True)  # Serializa el usuario asignado

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'title', 'description', 'assigned_to', 'start_date',
            'end_date', 'priority', 'status', 'estimated_hours', 'required_role'
        ]

# Serializer detallado para Project (incluye tareas anidadas)
class ProjectDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)  # Serializa todas las tareas relacionadas

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'priority', 'created_at', 'end_date',
            'created_by', 'tasks'
        ]

# Serializer detallado para Task (incluye proyecto anidado)
class TaskDetailSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)  # Serializa el proyecto relacionado
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'title', 'description', 'assigned_to', 'start_date',
            'end_date', 'priority', 'status', 'estimated_hours', 'required_role'
        ]