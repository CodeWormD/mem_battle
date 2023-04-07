from django.conf import settings
from django.core.mail import send_mail

SENDER = settings.EMAIL_HOST_USER


def confirm_mail(token, host, email_list):
    send_mail(
        subject='Confirm your account',
        message=f'Click the link to cofirm registration "http://{host}/api/auth/confirm/?token={token}"',
        from_email=SENDER,
        recipient_list=email_list,
        fail_silently=True
    )


def reset_password_email(email, host, link):
    send_mail(
        subject='Reset password',
        message=f'Click the link to cofirm registration "http://{host}{link}"',
        from_email=SENDER,
        recipient_list=email,
        fail_silently=True
    )