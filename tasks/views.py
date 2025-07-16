from django.shortcuts import render, redirect
from django.contrib import messages
from tasks.forms import TaskModelForm, TaskDetailsModelForm
from tasks.models import Task
from django.db.models import *
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

# Create your views here.
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employe(user):
    return user.groups.filter(name='Employee').exists()

@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status='COMPLETED').count()
    # in_progress_task = Task.objects.filter(status='IN_PROGRESS').count()
    # pending_task = Task.objects.filter(status='PENDING').count()

    type = request.GET.get('type', 'all')

    # getting task count
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING'))
    )

    # retrieving task data
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

    if type == 'all':
        tasks = base_query.all()
    elif type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')

    context = {
        'tasks': tasks,
        'counts': counts
    }
    return render(request, "dashboard/manager_dashboard.html", context)

@user_passes_test(is_employe, login_url='no-permission')
def employee_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

@login_required
@permission_required('tasks.add_task', login_url='no-permission')
def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()    #for GET
    task_details_form = TaskDetailsModelForm()    #for GET

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST)
        task_details_form = TaskDetailsModelForm(request.POST)

        if task_form.is_valid() and task_details_form.is_valid():
            """ For ModelForm Data """
            task = task_form.save()
            task_details = task_details_form.save(commit=False)
            task_details.task = task
            task_details.save()

            messages.success(request, 'Task Created Successfully.')
            return redirect('create-task')

    context = {'task_form': task_form, 'task_details_form': task_details_form}
    return render(request, "task_form.html", context)

@login_required
@permission_required('tasks.change_task', login_url='no-permission')
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)

    if task.details:
        task_details_form = TaskDetailsModelForm(instance=task.details)

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST, instance=task)
        task_details_form = TaskDetailsModelForm(request.POST, instance=task.details)

        if task_form.is_valid() and task_details_form.is_valid():
            """ For ModelForm Data """
            task = task_form.save()
            task_details = task_details_form.save(commit=False)
            task_details.task = task
            task_details.save()

            messages.success(request, 'Task Updated Successfully.')
            return redirect('update-task', id)

    context = {'task_form': task_form, 'task_details_form': task_details_form}
    return render(request, "task_form.html", context)

@login_required
@permission_required('tasks.delete_task', login_url='no-permission')
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully.')
        return redirect('manager-dashboard')
    else:
        messages.error(request, 'Something went wrong!')
        return redirect('manager-dashboard')

@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def view_task(request):
    task_count = Task.objects.aggregate(num_task=Count('id'))

    return render(request, "show_task.html", {'task_count': task_count})