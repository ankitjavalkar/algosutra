from rest_framework import serializers

from .models import Category, Task, TaskList

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList