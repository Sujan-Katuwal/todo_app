from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    status_choice = [
        ('pending', 'pending'),
        ('in_progress', 'in_progress'),
        ('completed', 'completed'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    assign_user = models.ManyToManyField(User, related_name='assigned_tasks')
    status = models.CharField(max_length=20, choices=status_choice, default='pending')


    def __str__(self):
        return self.title

