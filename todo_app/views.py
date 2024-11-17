from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


# Create your views here.
@login_required
def dashboard(request):
    # created_tasks = Task.objects.filter(assign_user=request.user)
    created_tasks = Task.objects.all()
    assigned_tasks = request.user.assigned_tasks.all()
    assigned_users = User.objects.all()
    return render(request, 'dashboard.html', {'created_tasks':created_tasks, 'assigned_tasks':assigned_tasks, 'assigned_users':assigned_users})

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST['deadline']
        assign_user_ids = request.POST.getlist('assign_user')
        assign_user = User.objects.filter(id__in=assign_user_ids)

        task = Task.objects.create(
            title = title,
            description = description,
            deadline = deadline
        )
        task.assign_user.set(assign_user)
        return redirect('dashboard')
    users = User.objects.all()
    return render(request, 'create_task.html', {'users':users})

@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task not in request.user.assign_tasks.all():
        return HttpResponseForbidden("You can not edit this task......")
    if request.method=='POST':
        task.status = request.POST['progress_status']
        task.save()
        return redirect('dashboard')
    return render(request, 'update_task_status.html', {'task':task})



# DRF API ViewSet
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import Taskserializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = Taskserializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['deadline', 'created_at']

    def get_queryset(self):
        return Task.objects.filter(assign_user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save()


