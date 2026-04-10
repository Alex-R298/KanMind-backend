"""URL configuration for the Kanban API."""

from django.urls import path

from kanban_app.api.views import (
    AssignedToMeView, BoardDetailView, BoardView,
    CommentDetailView, CommentView, ReviewingView,
    TaskDetailView, TaskView,
)

urlpatterns = [
    path('boards/', BoardView.as_view(), name='boards'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('tasks/', TaskView.as_view(), name='tasks'),
    path('tasks/assigned-to-me/', AssignedToMeView.as_view(), name='assigned-to-me'),
    path('tasks/reviewing/', ReviewingView.as_view(), name='reviewing'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:task_pk>/comments/', CommentView.as_view(), name='comments'),
    path('tasks/<int:task_pk>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
