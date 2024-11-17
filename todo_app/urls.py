from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import dashboard, create_task, update_task_status, TaskViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('create/', create_task, name='create_task'),
    path('update/<int:task_id>/', update_task_status, name='update_task_status'),
    path('api/', include(router.urls)),
]