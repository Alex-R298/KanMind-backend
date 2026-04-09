from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardView, TaskView, AssignedToMeView, ReviewingView, BoardDetailView, TaskDetailView
from auth_app.api.views import EmailCheckView

router = DefaultRouter()

urlpatterns = [
    path('boards/', BoardView.as_view(), name='boards'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('tasks/', TaskView.as_view(), name='tasks'),
    path('tasks/assigned-to-me/', AssignedToMeView.as_view(), name='assigned-to-me'),
    path('tasks/reviewing/', ReviewingView.as_view(), name='reviewing'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
