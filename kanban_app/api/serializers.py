"""Serializers for Board and Task models."""

from rest_framework import serializers

from kanban_app.models import Board, Task


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for creating and listing boards."""

    class Meta:
        model = Board
        fields = ['id', 'title', 'author', 'members']
        read_only_fields = ['author']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for creating and listing tasks."""

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status',
            'board', 'author', 'assigned_to', 'reviewer',
        ]
        read_only_fields = ['author']

