from rest_framework import serializers
from .models import User
# for login
from django.contrib.auth import authenticate
from django.contrib import auth

from rest_framework.exceptions import AuthenticationFailed

# for logout
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email','username','first_name','last_name', 'date_of_birth','gender','password']
# white spacing error should not include the def into meta class
    def validate(self,attrs):
        username = attrs.get('username','')
        if not username.isalnum():
            raise serializers.ValidationError('Username should only contain alphanumeric characters')
        return attrs    #missied this line
    def create(self,validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            date_of_birth = validated_data['date_of_birth'],
            gender = validated_data['gender'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200, min_length=3 )
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'username']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        
        user = auth.authenticate(username=username, password=password)
        
        # Check if the password is correct
        if user is None:
            raise AuthenticationFailed('Invalid password, try again')
            
        if not user.is_authorized:
            raise AuthenticationFailed('Your account has not been approved by an admin yet.')
            
        return {
            'email': user.email,
            'username': user.username,
             'tokens': user.tokens()
        }
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs.get('refresh')
        if not self.token:
            raise ValidationError('No token provided')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as e:
            raise serializer.ValidationError(str(e))