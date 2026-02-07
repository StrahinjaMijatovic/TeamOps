from django.contrib import admin
from .models import Project, Board, Column

class ColumnInline(admin.TabularInline):
    model = Column
    extra = 0

class BoardInline(admin.StackedInline):
    model = Board
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'owner', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'key')
    inlines = [BoardInline]

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('project', 'created_at')
    inlines = [ColumnInline]

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'board', 'order')
    list_filter = ('board__project',)
