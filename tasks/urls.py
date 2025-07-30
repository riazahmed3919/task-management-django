from django.urls import path
from .views import manager_dashboard, employee_dashboard, create_task, view_task, update_task, delete_task, task_details, dashboard, CreateTask, UpdateTask, ViewProject, TaskDetails

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('employee-dashboard/', employee_dashboard, name='employee-dashboard'),
    # path('create-task/', create_task, name='create-task'),
    path('create-task/', CreateTask.as_view(), name='create-task'),
    # path('update-task/<int:id>/', update_task, name='update-task'),
    path('update-task/<int:id>/', UpdateTask.as_view(), name='update-task'),
    # path('view-task/', view_task, name='view-task'),
    path('view-task/', ViewProject.as_view(), name='view-task'),
    # path('task/<int:task_id>/details/', task_details, name='task-details'),
    path('task/<int:task_id>/details/', TaskDetails.as_view(), name='task-details'),
    path('delete-task/<int:id>/', delete_task, name='delete-task'),
    path('dashboard/', dashboard, name='dashboard')
]