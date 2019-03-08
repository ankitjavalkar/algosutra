from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Category(models.Model):
    created_on = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    @staticmethod
    def get_all_categories_for_user(creator):
        return Category.objects.filter(creator=creator).order_by('-created_on')


class TaskList(models.Model):
    created_on = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    @staticmethod
    def get_all_task_list_for_user(creator):
        return TaskList.objects.filter(creator=creator).order_by('-created_on')


class Task(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('I', 'In Progress'),
        ('C', 'Complete'),
    )
    created_on = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField()
    target_date = models.DateField(default=datetime.date(datetime.now()))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P') 
    category = models.ForeignKey(
        Category, null=True, blank=True, related_name='tasks', on_delete=models.CASCADE
    )
    task_list = models.ForeignKey(
        TaskList, null=True, blank=True, related_name='tasks', on_delete=models.CASCADE
    )

    @staticmethod
    def get_all_tasks_for_user(creator):
        return Task.objects.filter(creator=creator).order_by('-created_on')

    @staticmethod
    def get_all_tasks_due_on(creator, date):
        return Task.objects.filter(
            creator=creator,
            target_date=date,
        ).order_by('-created_on')
