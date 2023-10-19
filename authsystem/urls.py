from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
     
    path("token/", TokenObtainPairView.as_view(), name= "token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name= "token_refresh"),
    path("register/",RegisterView.as_view(), name="registerView"),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]
