import pytest
from django import urls
from django.core import mail
from apps.users.models import User


class TestUserAuth:
    url_signup = urls.reverse('signup')
    url_confirm_code = urls.reverse('confirm')


    @pytest.mark.django_db(transaction=True)
    def test_signup_nodata(self, client):
        """Check behavior with no data sent"""
        response = client.post(self.url_signup)
        request_type = 'POST'

        assert response.status_code != 404, (
            f'Check that {self.url_signup} is exist'
        )
        assert response.status_code == 400, (
            f'No data with {self.request_type} should return status 400'
        )
        response_json = response.json()
        empty_fields = ['username', 'password', 'password_repeat', 'email']

        for field in empty_fields:
            assert field in response_json, (
                f'{self.request_type} with no data should return message with fields required'
            )

    @pytest.mark.django_db(transaction=True)
    def test_user_signup_invalid_data(self, client):
        """Check invalid data send exceptions"""
        invalid_password = '1111'
        invalid_password_repeat = '111'
        invalid_email = 'mymail.fake'
        invalid_username = 'usernamefake'

        request_type = 'POST'

        invalid_data = {
            'username': invalid_username,
            'password': invalid_password,
            'password_repeat': invalid_password_repeat,
            'email': invalid_email
        }
        code = 400
        response = client.post(self.url_signup, invalid_data)
        assert response.status_code == code, (
            f'Check sending {self.request_type} to {self.url_signup}'
            f'should return code {code}'
        )

        response_json = response.json()
        invalid_fields = ['email']
        for field in invalid_fields:
            assert field in response.json(), (
                f'Check that valid {field} is required'
            )

        invalid_data_password = {
            'username': invalid_username,
            'password': invalid_password,
            'password_repeat': invalid_password_repeat,
            'email': 'validemail@mail.ru'
        }
        response = client.post(self.url_signup, invalid_data_password)
        response_json = response.json()
        invalid_field = ['non_field_errors']
        for field in invalid_field:
            assert field in response_json, (
                'Check that it is required equal passwords'
            )

        invalid_data_email = {
            'username': invalid_username,
            'password': invalid_password,
            'password_repeat': invalid_password_repeat
        }
        response = client.post(self.url_signup, invalid_data_email)
        response_json = response.json()
        required_field = ['email']
        for field in required_field:
            assert field in response_json, (
                f'Check that you can not {request_type} without email'
                'and get email required error.'
            )

        invalid_data_username = {
            'password': '12345qwe',
            'password_repeat': '12345qwe',
            'email': 'validemail@mail.ru'
        }
        response = client.post(self.url_signup, invalid_data_username)
        response_json = response.json()
        required_field = ['username']
        for field in required_field:
            assert field in response_json, (
                f'Check that you can not {request_type} without username'
                'and get username required error.'
            )

    @pytest.mark.django_db(transaction=True)
    def test_user_signup(self, client, user_data1):
        """Signup and mail sending check"""
        mail_count_before = len(mail.outbox)
        response = client.post(self.url_signup, user_data1)
        mail_count_after = len(mail.outbox)

        response_json = response.json()
        message = ['Message']
        for value in message:
            assert response_json[value] == 'User have been created, check your email to verify', (
                'Check that you get a success message after',
                'register new user'
            )

        assert mail_count_after != mail_count_before, (
            'Check that you send email to user email')

        response = client.post(self.url_signup, user_data1)
        assert response.status_code == 400, (
            'Check that email and yusername are unique',
            'and user can not register twice one email'
        )
        response_json = response.json()
        invalid_field = ['email', 'username']
        for field in invalid_field:
            assert field in response_json, (f'Check that {field} is unique')

        email = user_data1['email']
        new_user = User.objects.get(email=email)
        assert isinstance(new_user, User), (
            f'Check that after registration new user with email {email} created'
        )
        assert new_user.is_verified == False, (
            'Check that user is not verified after registration'
        )