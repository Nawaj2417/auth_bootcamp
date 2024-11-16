from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import *
# login import
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken     #imported refresh token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username = serializer.validated_data['username'])
        
        if user.is_authorized:
            response_data = serializer.validated_data
            response_data['detail'] = 'Logged in successfully'

            refresh = RefreshToken.for_user(user)
            user.refresh_token = str(refresh)
            user.save()
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie('refreshToken', user.refresh_token, secure=True, samesite='None')
            return response
        else:    
            return Response({"detail":"Your account has not been approved by an admin yet"},status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    @permission_classes([AllowAny])     #Any one can access this 

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)