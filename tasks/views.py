from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task

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

            """ For TaskForm """
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')

            # task = Task.objects.create(title=title, description=description, due_date=due_date)
            
            # #assigned employees to task
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)

            # return HttpResponse("Task added successfully.")

    context = {'form': form}
    return render(request, "task_form.html", context)