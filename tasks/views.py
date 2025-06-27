from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetails
from datetime import date
from django.db.models import Q

# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

def test(request):
    names = ['Rahim', 'Karim', 'Jabbar', 'Sattar', 'Mr. Alu']
    count = 0
    for name in names:
        count += 1
    context = {
        'names': names,
        'age': [10, 20, 30, 40, 50],
        'count': count
    }
    return render(request, "test.html", context)

def create_task(request):
    # employees = Employee.objects.all()
    form = TaskModelForm()    #for GET

    if request.method == 'POST':            #for POST
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """ For TaskModelForm """
            form.save()
            return render(request, 'task_form.html', {'form': form, 'message': "Task Added Successfully."})

    context = {'form': form}
    return render(request, "task_form.html", context)

def view_task(request):
    """ show the task that contain the word '___' """
    # tasks = Task.objects.filter(title__icontains='ie')

    """ show the task that contain the word '___' and status '___' """
    # tasks = Task.objects.filter(title__icontains='ie', status='PENDING')

    """ show the task that status is PENDING or IN_PROGRESS """
    tasks = Task.objects.filter(Q(status='PENDING') | Q(status='IN_PROGRESS'))

    return render(request, "show_task.html", {'tasks': tasks})