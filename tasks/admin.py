from django.contrib import admin
from .models import Task, Label

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'column', 'assignee', 'priority', 'due_date', 'created_by')
    list_filter = ('priority', 'project', 'column')
    search_fields = ('title', 'description')
