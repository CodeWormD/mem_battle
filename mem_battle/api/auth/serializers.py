from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        write_only=True,
    )
    password_repeat = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password_repeat',
            'email',
        )

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_repeat'):
            raise serializers.ValidationError('Passwords must be equal')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_repeat')
        return User.objects.create_user(**validated_data)



class UserCodeConfirmSerializer(serializers.ModelSerializer):
    token = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ('token',)


class UserRestPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email',)


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )
    uidb64 = serializers.CharField(
        write_only=True
    )
    token = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = ('password', 'uidb64', 'token')

    def update(self, instance, validated_data):
        instance.password = validated_data.get('password')
        instance.save()
        return instance


class UserLogoutSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()

    class Meta:
        model = User
        fields = ('refresh',)

    def save(self):
        refresh = self.validated_data['refresh']
        RefreshToken(refresh).blacklist()

