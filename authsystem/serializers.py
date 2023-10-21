from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 20, write_only = True)
    class Meta:
        model = User
        fields = ["username", "name", "email", 'role',"password", "Cnic", "Phone_number", "city"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            Cnic=validated_data["Cnic"],
            name=validated_data["name"]
        )
        return user

class LogInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    password = serializers.CharField(max_length = 20, write_only = True)
    username = serializers.CharField(max_length= 30, read_only = True)
    tokens = serializers.CharField(max_length = 255, read_only = True)


    class Meta:
        model = User
        fields = ['email','username', 'password', 'tokens']
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')

        user= auth.authenticate(email=email, password= password)

        return {
            'email':user.email,
            'username' : user.username,
            'tokens': user.tokens()
        }
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20,  write_only=True)
    token  = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    
    class Meta:
        fields =['password','token','uidb64']

    def validate(self, attrs):
        password = attrs.get('password')
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')

        id =  force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id = id)

        if not PasswordResetTokenGenerator().check_token(user,token):
            return "the reset Link is invalid"
        
        user.set_password(password)
        user.save()
        
        return user

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ['email']

   

       