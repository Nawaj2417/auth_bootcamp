from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
# from .views import *
urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/', views.LoginAPIView.as_view(),name="login"),
    path('logout/', views.LogoutAPIView.as_view(),name="logout"),
    
]
