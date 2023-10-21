from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class User(AbstractUser):
    Role_Choices = (
        ('Captain','Captain'),
        ('Player',"player")
    )
    username = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, choices=Role_Choices)
    Cnic = models.CharField(max_length=30, null= True, blank=True)
    Phone_number = models.IntegerField(null= True, blank=True)
    email = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=30,null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    def tokens(self):
        tokens = RefreshToken.for_user(self)
        return ''

class ResetToken(models.Model):
    username = models.ForeignKey(User, models.CASCADE)
    token = models.CharField(max_length=255, null= True)
    created_at = models.DateTimeField()