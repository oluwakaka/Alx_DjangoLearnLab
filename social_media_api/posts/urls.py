from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentViewSet,
    FeedView,
    LikePostView,
    UnlikePostView,
)

# Use DRF router for Post and Comment viewsets
router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),

    # Feed endpoint
    path("feed/", FeedView.as_view(), name="feed"),

    # Like/Unlike endpoints
    path("posts/<int:post_id>/like/", LikePostView.as_view(), name="like-post"),
    path("posts/<int:post_id>/unlike/", UnlikePostView.as_view(), name="unlike-post"),
]
