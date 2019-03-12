from datetime import datetime

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404, redirect

from .models import Category, Task, TaskList
from .forms import CategoryForm, TaskForm, TaskListForm


def dashboard(request):
    user = request.user
    latest_due_tasks = Task.get_all_tasks_due_on(
        user,
        datetime.date(datetime.now()),
    )
    completed_task_count = Task.objects.filter(status='C').count()
    in_progress_task_count = Task.objects.filter(status='I').count()
    pending_task_count = Task.objects.filter(status='P').count()
    context = {
        'completed_task_count': completed_task_count,
        'in_progress_task_count': in_progress_task_count,
        'pending_task_count': pending_task_count,
        'latest_due_tasks': latest_due_tasks,
    }

    return render(request, 'dashboard.html', context)


def tasks(request):
    user = request.user
    tasks = Task.get_all_tasks_for_user(user)

    return render(request, 'tasks.html', {'tasks': tasks})


def task_detail(request, task_id=None):
    user = request.user
    if task_id:
        task = get_object_or_404(Task, pk=task_id, creator=user)
    else:
        task = None

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            if task is None:
                form.instance.creator = user
            form.save()
            task = form.instance
        return redirect('todo:task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'task.html', {'form': form,})


def task_lists(request):
    user= request.user
    task_lists = TaskList.get_all_task_list_for_user(user)

    return render(request, 'task_lists.html', {'task_lists': task_lists})


def task_list_detail(request, task_list_id=None):
    user = request.user
    if task_list_id:
        task_list = get_object_or_404(TaskList, pk=task_list_id, creator=user)
    else:
        task_list = None

    if request.method == 'POST':
        form = TaskListForm(request.POST, instance=task_list)
        if form.is_valid():
            if task_list is None:
                form.instance.creator = user
            form.save()
            task_list = form.instance
        return redirect('todo:task_list_detail', task_list_id=task_list.id)
    else:
        form = TaskListForm(instance=task_list)

    return render(request, 'task_list_detail.html', {'form': form,})

def categories(request):
    user= request.user
    categories = Category.get_all_categories_for_user(user)

    return render(request, 'dashboard.html', {'categories': categories})


def category_detail(request, category_id=None):
    user = request.user
    if category_id:
        category = get_object_or_404(Category, pk=category_id, creator=user)
    else:
        category = None

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            if category is None:
                form.instance.creator = user
            form.save()
            category = form.instance
        return redirect('todo:category_detail', category_id=category.id)
    else:
        form = CategoryForm(instance=category)

    return render(request, 'category.html', {'form': form,})
