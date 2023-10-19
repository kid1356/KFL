from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import RegisterSerializer,ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
# Create your views here.



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self,queryset = None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():

            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ["wrong password"]}, status = status.HTTP_400_BAD_REQUEST)
            
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            response = {
                'status' : 'success',
                'code' : status.HTTP_200_OK,
                'message' : 'Password updated',
                'data' : []
            }

            return Response(response)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )