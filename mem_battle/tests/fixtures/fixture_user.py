import pytest


@pytest.fixture
def user_superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        username='TestSuperuser',
        email='testsuperuser@bk.fake',
        password='1234567',
        is_verified=True,
    )

@pytest.fixture
def user_1(django_user_model):
    return django_user_model.objects.create_user(
        username='daniil',
        email='dan1.d@bk.ru',
        password='819224425298q'
    )

@pytest.fixture
def user_data1():
    data = {
        "username": "daniil",
        "email":"dan1.d@bk.ru",
        "password": "819224425298q",
        "password_repeat": "819224425298q"
    }
    return data
