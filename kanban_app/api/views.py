"""Views for the Kanban board API."""

from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from kanban_app.api.permissions import IsAuthor, IsBoardMember
from kanban_app.api.serializers import (
    BoardSerializer, CommentSerializer, TaskSerializer,
)
from kanban_app.models import Board, Comment, Task


def is_board_member(user, board):
    """Return True if user is author or member of the board."""
    return board.author == user or board.members.filter(
        pk=user.pk,
    ).exists()


class BoardView(APIView):
    """List boards for the current user or create a new board."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return boards where user is author or member."""
        boards = Board.objects.filter(
            Q(author=request.user) | Q(members=request.user),
        ).distinct()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new board with the current user as author."""
        serializer = BoardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a single board."""

    permission_classes = [IsAuthenticated, IsBoardMember, IsAuthor]
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class TaskView(APIView):
    """List tasks for the current user or create a new task."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return tasks where the user is the board author."""
        tasks = Task.objects.filter(board__author=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new task with the current user as author."""
        board = self._get_board(request)
        if board is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not is_board_member(request.user, board):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_board(self, request):
        """Return the board from request data or None."""
        board_id = request.data.get('board')
        try:
            return Board.objects.get(pk=board_id)
        except (Board.DoesNotExist, ValueError, TypeError):
            return None


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a single task."""

    permission_classes = [IsAuthenticated, IsAuthor]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class AssignedToMeView(APIView):
    """List tasks assigned to the current user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return tasks where assigned_to is the current user."""
        assigned = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(assigned, many=True)
        return Response(serializer.data)


class ReviewingView(APIView):
    """List tasks where the current user is reviewer."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return tasks where reviewer is the current user."""
        reviewing = Task.objects.filter(reviewer=request.user)
        serializer = TaskSerializer(reviewing, many=True)
        return Response(serializer.data)


class CommentView(APIView):
    """List or create comments for a specific task."""

    permission_classes = [IsAuthenticated]

    def get(self, request, task_pk):
        """Return all comments for the given task."""
        task = self._get_task(task_pk)
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not is_board_member(request.user, task.board):
            return Response(status=status.HTTP_403_FORBIDDEN)
        comments = Comment.objects.filter(task=task)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, task_pk):
        """Create a comment on the given task."""
        task = self._get_task(task_pk)
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not is_board_member(request.user, task.board):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(author=request.user, task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_task(self, task_pk):
        """Return the task or None if not found."""
        try:
            return Task.objects.get(pk=task_pk)
        except Task.DoesNotExist:
            return None


class CommentDetailView(generics.DestroyAPIView):
    """Delete a single comment."""

    permission_classes = [IsAuthenticated, IsAuthor]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer