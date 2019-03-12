from django.contrib import admin

from .models import Category, Task, TaskList

admin.site.register(Task)
admin.site.register(TaskList)
admin.site.register(Category)

