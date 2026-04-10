"""Models for the Kanban board application."""

from django.conf import settings
from django.db import models


class Board(models.Model):
    """A Kanban board owned by a user with optional members."""

    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="boards")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="shared_boards", blank=True)

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        ordering = ["title"]

    def __str__(self):
        """Return the board title."""
        return self.title


class Task(models.Model):
    """A task belonging to a board with assignee and reviewer."""

    STATUS_CHOICES = [
        ("to-do", "To Do"),
        ("in-progress", "In Progress"),
        ("review", "Review"),
        ("done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="to-do")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_tasks")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="assigned_tasks", null=True, blank=True)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="reviewing_tasks", null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-id"]

    def __str__(self):
        """Return the task title."""
        return self.title


class Comment(models.Model):
    """A comment on a task."""

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self):
        """Return a description of the comment."""
        return f"Comment by {self.author} on {self.task}"
