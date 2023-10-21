from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
     
    path("token/", TokenObtainPairView.as_view(), name= "token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name= "token_refresh"),
    path("register/",RegisterView.as_view(), name="registerView"),
    path('change-password/', PasswordResetView.as_view(), name='change_password'),
    path('login/', LogInView.as_view(), name= "login"),
    path("password-reset/<uidb64>/<token>/", PasswordTokenAPIView.as_view(),  name= 'password_reset_confirm'),
    path("reset-password-email", PasswordResetEmailView.as_view(), name = 'reset-password-email'),
    path('passowrd-reset-complete', SetNewPasswordView.as_view(), name = 'passowrd-reset-complete'),

]
