from django.shortcuts import render, redirect
from django.contrib import messages
from tasks.forms import TaskModelForm, TaskDetailsModelForm
from tasks.models import Task, Project
from django.db.models import *
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView

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
        'counts': counts,
        'role': 'manager'
    }
    return render(request, "dashboard/manager_dashboard.html", context)

@user_passes_test(is_employe, login_url='no-permission')
def employee_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

@login_required
@permission_required('tasks.add_task', login_url='no-permission')
def create_task(request):
    task_form = TaskModelForm()    #for GET
    task_details_form = TaskDetailsModelForm()    #for GET

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST)
        task_details_form = TaskDetailsModelForm(request.POST, request.FILES)

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

# CBV for Create Task
class CreateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'
    template_name = 'task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_details_form'] = kwargs.get('task_details_form', TaskDetailsModelForm())

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_details_form = TaskDetailsModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_details_form.is_valid():
            """ For ModelForm Data """
            task = task_form.save()
            task_details = task_details_form.save(commit=False)
            task_details.task = task
            task_details.save()

            messages.success(request, 'Task Created Successfully.')
            context = self.get_context_data(task_form=task_form, task_details_form=task_details_form)
            return render(request, 'create_task.html', context)

@login_required
@permission_required('tasks.change_task', login_url='no-permission')
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)

    if task.details:
        task_details_form = TaskDetailsModelForm(instance=task.details)

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST, instance=task)
        task_details_form = TaskDetailsModelForm(request.POST, request.FILES, instance=task.details)

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

# CVB for Update Task
class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()

        if hasattr(self.object, 'details') and self.object.details:
            context['task_details_form'] = TaskDetailsModelForm(instance=self.object.details)
        else:
            context['task_details_form'] = TaskDetailsModelForm()

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)

        task_details_form = TaskDetailsModelForm(
            request.POST, request.FILES, instance=getattr(self.object, 'details', None))
        
        if task_form.is_valid() and task_details_form.is_valid():
            """ For ModelForm Data """
            task = task_form.save()
            task_details = task_details_form.save(commit=False)
            task_details.task = task
            task_details.save()

            messages.success(request, 'Task Updated Successfully.')
            return redirect('update-task', self.object.id)
        
        return redirect('update-task', self.object.id)

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
    projects = Project.objects.annotate(
        num_task=Count('task')).order_by('num_task')
    return render(request, "show_task.html", {"projects": projects})

# CVB for View Project
view_project_decorators = [login_required, permission_required('projects.view_project', login_url='no-permission')]
@method_decorator(view_project_decorators, name='dispatch')
class ViewProject(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'show_task.html'

    def get_queryset(self):
        queryset = Project.objects.annotate(
            num_task=Count('task')).order_by('num_task')
        return queryset

@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choice = Task.STATUS_CHOICES
    if request.method == 'POST':
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect( 'task-details', task.id)
    
    return render(request, 'task_details.html', {'task': task, 'status_choices': status_choice})

# CVB for Task Details
task_details_decorators = [login_required, permission_required('tasks.view_task', login_url='no-permission')]
@method_decorator(task_details_decorators, name='dispatch')
class TaskDetails(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choice'] = Task.STATUS_CHOICES

        return context
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)

@login_required # no need CBV
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employe(request.user):
        return redirect('employee-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    else:
        return redirect('no-permission')