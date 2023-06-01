from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .comments import views
from .groups import views as group_view
from .mems import views as mem_view
from .tags import views as tag_view

router = DefaultRouter()
router.register('mems', mem_view.MemsViewSet, basename='mems')
router.register('groups', group_view.GroupModelViewSet, basename='groups')
router.register('tags', tag_view.TagViewSet, basename='tags')


urlpatterns = [
    path('v1/', include(router.urls)),

    path('v1/mems/<uuid:mem_id>/like/',
         mem_view.MemLikeAPIView.as_view()),
    path('v1/mems/<uuid:mem_id>/dislike/',
         mem_view.MemDisLikeAPIView.as_view()),

    path('v1/mems/<uuid:mem_id>/comments/',
         views.CommentListCreateAPIView.as_view()),
    path('v1/mems/<uuid:mem_id>/comments/<uuid:comment_id>/',
         views.CommentCUDAPIView.as_view()),
    path('v1/mems/<uuid:mem_id>/comments/<uuid:comment_id>/like/',
         views.CommentLikeAPIView.as_view()),
    path('v1/mems/<uuid:mem_id>/comments/<uuid:comment_id>/dislike/',
         views.CommentDisLikeAPIView.as_view()),
]