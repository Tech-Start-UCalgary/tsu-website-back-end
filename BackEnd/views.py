from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view


# Create your views here. 
# Event Section Views
class saveEventSection(generics.CreateAPIView):
    queryset = EventSection.objects.all()
    serializer_class = EventSectionSerializer

class getEventSection(generics.ListAPIView):
    queryset = EventSection.objects.all()
    serializer_class = EventSectionSerializer

class deleteEventSection(generics.DestroyAPIView):
    queryset = EventSection.objects.all()
    serializer_class = EventSectionSerializer

class updateEventSection(generics.RetrieveUpdateAPIView):
    queryset = EventSection.objects.all()
    serializer_class = EventSectionSerializer

# Event Views
class saveEvent(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializerWithEventSectionId

class getEvent(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class deleteEvent(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class updateEvent(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializerWithEventSectionId

# Comment Views
class saveComment(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializerWithPostAndAuthorId

class getComment(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class deleteComment(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class updateComment(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializerWithPostAndAuthorId

# Post Views
class createUserPost(generics.CreateAPIView):
    def get_queryset(self):
        queryset = Post.objects.all()
        queryset = queryset.filter(author=self.request.user)
	# Leftside of filter: from queryset. Rightside: how we're filtering
        return queryset
    serializer_class = PostSerializerWithAuthorId

class getPost(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class updateUserPost(generics.RetrieveUpdateAPIView):
    def get_queryset(self):
        queryset = Post.objects.all()
        queryset = queryset.filter(author=self.request.user)
	# Leftside of filter: from queryset. Rightside: how we're filtering
        return queryset
    serializer_class = PostSerializerWithAuthorId

class deleteUserPost(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Post.objects.all()
        queryset = queryset.filter(author=self.request.user)
	# Leftside of filter: from queryset. Rightside: how we're filtering
        return queryset
    serializer_class = PostSerializer

# Register User View
class RegisterUserView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RegisterSerializer 

# Return User ID, First Name and Last Name 
class customObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        response = super(customObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id, 'first': user.first_name, 'last': user.last_name})

def pingAppView(request):
    return HttpResponse("")