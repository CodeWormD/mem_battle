import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, smart_bytes,
                                   smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.cores.exceptions import (MailSendingException, UserAlreadyVerified,
                                   UserDoesNotExist)
from apps.users.models import User
from utils.email_body import confirm_mail, reset_password_email

from .serializers import (SetNewPasswordSerializer, UserRegistrationSerializer,
                          UserRestPasswordSerializer, UserLogoutSerializer)
from apps.cores.validators import validate_token_user


@api_view(['POST'])
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    email = serializer.data['email']

    user = User.objects.get(email=email)

    token = RefreshToken.for_user(user=user)

    try:
        confirm_mail(
            host=request.get_host(),
            token=token,
            email_list=[email]
        )
    except MailSendingException:
        return Response(
            {'Error': 'Mail to user does not send'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {'Message': 'User have been created, check your email to verify'},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
def user_confirm_code(request):
    token = request.GET.get('token')

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        id = payload['user_id']
    except jwt.exceptions.DecodeError:
        return Response(
            {'Error': 'Invalid Token'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(id=id)
    except UserDoesNotExist:
        return Response(
            {'Error': 'User not found'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        if user.is_verified==False:
            user.is_verified = True
            user.save()
            return Response(
                {'Confirmation status': 'Success'},
                status=status.HTTP_200_OK
            )
    except UserAlreadyVerified:
        return Response(
            {'Error': 'User already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def user_reset_password(request):
    serializer = UserRestPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.data['email']

    user = User.objects.get(email=email)

    if user:
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        relativeLink = reverse(
                'reset-password',
                kwargs={'uidb64': uidb64,
                        'token': token})

        reset_password_email(
            host=request.get_host(),
            email=[user.email],
            link=relativeLink
        )
    return Response(
        {'Status': 'Email has been sent. Check your email to reset password'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def user_reset_verify(request, uidb64, token):
    try:
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response(
                {'Token': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'Success': True,
            'message': 'Credentials Valid',
            'uidb64': uidb64,
            'token': token
        }, status=status.HTTP_200_OK)

    except DjangoUnicodeDecodeError:
            return Response(
                {'error': 'Token is not valid, please request a new one'},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['PATCH'])
def user_reset_complete(request):
    user = request.data.get('uidb64')
    token = request.data.get('token')

    user_id = smart_str(urlsafe_base64_decode(user))
    user = User.objects.get(id=user_id)

    validate_token_user(token, user)

    serializer = SetNewPasswordSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        {'success': True, 'message': 'Password reset successfully'},
        status=status.HTTP_200_OK)


@api_view(['POST'])
def user_logout(request):
    serializer = UserLogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        serializer.save()
    except TokenError:
        return Response(
            {'Error': 'No such token or it has been expired'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {'Message': 'You are logout'},
        status=status.HTTP_204_NO_CONTENT
    )

