from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from kanban_app.api.serializers import BoardSerializer, TaskSerializer
from kanban_app.models import Board, Task
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics




class BoardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(members=request.user)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task = Task.objects.filter(board__author=request.user)
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class AssignedToMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assigned = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(assigned, many=True)
        return Response(serializer.data)
    


class ReviewingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviewing = Task.objects.filter(reviewer=request.user)
        serializer = TaskSerializer(reviewing, many=True)
        return Response(serializer.data)