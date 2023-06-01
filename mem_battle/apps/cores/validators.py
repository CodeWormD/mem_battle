from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import User

from .exceptions import UserDoesNotExist


def validate_token_user(token, user):
    """Check token and user id for reset password"""

    if not user:
        raise UserDoesNotExist('Invalid user id', 404)

    if not PasswordResetTokenGenerator().check_token(user, token):
        raise AuthenticationFailed('The reset link is invalid', 401)