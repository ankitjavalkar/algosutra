from django import forms
from django.contrib.auth.models import User

from .models import Category, Task, TaskList


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['creator', 'created_on']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['creator', 'created_on']


class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        exclude = ['creator', 'created_on']
