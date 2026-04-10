"""Serializers for Board and Task models."""

from django.contrib.auth.models import User
from rest_framework import serializers

from kanban_app.models import Board, Task, Comment


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for user as board member."""

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """Return combined first and last name."""
        return f"{obj.first_name} {obj.last_name}".strip()


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for creating and listing tasks."""

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to',
        write_only=True, required=False, allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer',
        write_only=True, required=False, allow_null=True,
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'board', 'author', 'assignee_id', 'reviewer_id', 'due_date',
            'comments_count',
        ]
        read_only_fields = ['author']

    def get_comments_count(self, obj):
        """Return number of comments on this task."""
        return obj.comments.count()

    def to_representation(self, instance):
        """Return assignee/reviewer as nested objects."""
        data = super().to_representation(instance)
        data['assignee'] = MemberSerializer(instance.assigned_to).data if instance.assigned_to else None
        data['reviewer'] = MemberSerializer(instance.reviewer).data if instance.reviewer else None
        return data


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for creating and listing boards."""

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='author.id', read_only=True)

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'author', 'members', 'member_count',
            'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count',
            'owner_id',
        ]
        read_only_fields = ['author']

    def get_member_count(self, obj):
        """Return number of board members."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Return total task count."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Return count of tasks with to-do status."""
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        """Return count of high-priority tasks."""
        return obj.tasks.filter(priority="high").count()

    def to_representation(self, instance):
        """Return members as nested objects and include tasks."""
        data = super().to_representation(instance)
        data['members'] = MemberSerializer(instance.members.all(), many=True).data
        data['tasks'] = TaskSerializer(instance.tasks.all(), many=True).data
        return data
    

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for task comments."""

    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']

    def get_author(self, obj):
        """Return author fullname."""
        return f"{obj.author.first_name} {obj.author.last_name}".strip()