from rest_framework import generics, permissions
from .serializers import Todoserializer, TodoCompleteserializer
from todo.models import Todo
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
import json
from rest_framework.response import Response
from django.contrib.auth import authenticate

# in case of APIs we don't have to worry about csrf token hence we exempt csrf
"""@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            #data = JSONParser().parse(request)
            #user = User.objects.create_user(data['username'], password=data['password'])
            print(request)
            user = User.objects.create_user(request.data['username'], password=request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error':'That username has already been taken. Please choose a new username'}, status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        #data = json.loads(request.body)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'error': 'Could not login.'},status=400)
        else:
            try:
                Token.objects.get(user = user)
            except:
                Token.objects.create(user = user)
        #token = Token.objects.create(user=user)
            return Response({'token':'hbchbc'})""""

            
class completedList(generics.ListAPIView):
    serializer_class = Todoserializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        #return Todo.objects.filter(user = user, datecompleted != None).order_by('-datecompleted')
        return Todo.objects.filter(user = user, datecompleted__isnull= False).order_by('-datecompleted')


class currentTodos(generics.ListCreateAPIView):
    serializer_class = Todoserializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user = user, datecompleted__isnull = True)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Todoserializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        #return Todo.objects.filter(user = user, datecompleted != None).order_by('-datecompleted')
        return Todo.objects.filter(user = user)

class completedTodo(generics.UpdateAPIView):
    serializer_class = TodoCompleteserializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        #return Todo.objects.filter(user = user, datecompleted != None).order_by('-datecompleted')
        return Todo.objects.filter(user = user)

    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()
    
