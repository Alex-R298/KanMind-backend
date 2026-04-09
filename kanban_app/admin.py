"""Admin configuration for the Kanban app."""

from django.contrib import admin

from .models import Board, Task


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """Admin view for Board model."""

    list_display = ['title', 'author']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin view for Task model."""

    list_display = ['title', 'status', 'board', 'assigned_to', 'reviewer']
    list_filter = ['status', 'board']
