from django.contrib.auth.models import AbstractUser, Group
from django.db import models


# class UserRole(models.Model):

#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_user = models.BooleanField(default=True)
#     description = models.TextField(verbose_name='Описание роли')
#     # role = models.CharField(
#     #     verbose_name='Роль пользователя',
#     #     max_length=25,
#     #     )


# class User(AbstractUser):

#     username = models.TextField(
#         verbose_name='User nickname',
#         blank=True,
#         null=True,
#         unique=True
#     )
#     email = models.EmailField(
#         verbose_name='User email',
#         unique=True,
#     )
    # role = models.ForeignKey(
    #     UserRole,
    #     verbose_name='User role',
    #     related_name='users',
    #     default=UserRole.is_user,
    #     on_delete=models.SET_NULL
    # )
