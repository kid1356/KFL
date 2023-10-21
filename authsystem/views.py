from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import *
# Create your views here.





from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, ResetToken
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class PasswordResetView(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        
        if username:
            try:
                user = User.objects.get(username=username)
                # Generate and save the reset token for the user
                token, created = ResetToken.objects.get_or_create(user=user)
                return Response({"message": "Password reset token generated successfully"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Missing 'username' in the request"}, status=status.HTTP_400_BAD_REQUEST)

    
 
class LogInView(generics.GenericAPIView):
    serializer_class = LogInSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        
        return Response(serializer.data,  status=status.HTTP_200_OK)


class PasswordResetEmailView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer
    def post(self, request):
        serializer = self.serializer_class(data=  request.data)

        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email= email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relativelink = reverse('password_reset_confirm', kwargs={'uidb64':uidb64 , 'token':token})
            absurl = 'htttp://'+ current_site + relativelink
            email_body = "hi,  \n Use This Link below to reset your password \n"  + absurl
            data = {"email_body": email_body, "to_email":user.email,"email_subject" :"reset your password"}

            Util.send_mail(data)

        return Response({"success": "we have sent You a link to reset password"}, status=status.HTTP_200_OK)

class PasswordTokenAPIView(generics.GenericAPIView):
    def get(self, request, uidb64,token):
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            return Response({'error':'Token is not valid, please request a new one!'})
        return Response({'success':True, 'message':'Credentials valid', 'uidb64': uidb64,'token':token},status=status.HTTP_200_OK)
        
class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'success':True, 'message': 'password reset is successfully'}, status=status.HTTP_200_OK)
