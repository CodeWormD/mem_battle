from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .mems.views import MemsViewSet, CommentViewSet


router = DefaultRouter()
router.register('mems', MemsViewSet, basename='mems')
router.register('comments', CommentViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]