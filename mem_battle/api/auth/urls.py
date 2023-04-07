from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .auth import (user_confirm_code, user_registration, user_reset_complete,
                   user_reset_password, user_reset_verify, user_logout)

urlpatterns = [
    path('auth/signup/', user_registration, name='signup'),
    path('auth/confirm/', user_confirm_code, name="confirm"),
    path('auth/reset-password-send/', user_reset_password, name="reset-password-send"),
    path('auth/reset-password/<uidb64>/<token>/', user_reset_verify, name="reset-password"),
    path('auth/reset-password-complete/', user_reset_complete, name="reset-password-complete"),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', user_logout, name='logout'),
]