# Project Manager

## Autor: Juan Araujo

## Descripción del Proyecto

**Project Manager** es una aplicación diseñada para facilitar la gestión y asignación de tareas en un entorno empresarial. Este sistema permite a los administradores crear proyectos, añadir tareas específicas y asignarlas a los empleados según sus roles. Entre las principales funcionalidades, se incluye una opción de **optimización de tareas**, que asigna automáticamente tareas a los empleados basándose en los siguientes criterios:

1. **Rol Compatible**: Solo se asignan tareas que requieran el mismo rol que el empleado.
2. **Carga de Trabajo Equilibrada**: Se prioriza a los empleados que no tengan tareas asignadas o que tengan una baja carga de trabajo.

El objetivo principal es maximizar la eficiencia del equipo y garantizar que las tareas sean asignadas de manera justa y precisa.

---

## Características Principales

- **Gestión de Proyectos**: Crea, edita y elimina proyectos.
- **Gestión de Empleados**: Añade, edita y elimina empleados con sus respectivos roles.
- **Asignación Manual de Tareas**: Permite a los administradores asignar tareas específicas a los empleados.
- **Optimización Automática**: Asigna tareas automáticamente según el rol del empleado y su carga de trabajo.
- **Interfaz Intuitiva**: Una interfaz fácil de usar para la gestión de proyectos y tareas.

---

## Instalación

Sigue los pasos a continuación para instalar y configurar el proyecto en tu entorno local:

### Requisitos Previos

- **Python 3.8 o superior** instalado en tu sistema.
- Un entorno virtual para gestionar dependencias (opcional pero recomendado).

### Instrucciones de Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/ProjectManagerPro.git
   cd ProjectManagerPro
   
2. **Crear un entorno virtual (si el caso lo amerita)**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   
3. **Instalar las dependencias**:
   ```bash
    pip install -r requirements.txt
    ```
   
4. **Configurar la Base de Datos**:
    ```bash
    python manage.py migrate
    ```

5. **Ejecutar el Servidor de Desarrollo**:
    ```bash
    python manage.py runserver
    ```
   
7. Ahora puedes empezar a utilizar Project Manager.


