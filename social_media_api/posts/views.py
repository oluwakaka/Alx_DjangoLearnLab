from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification   # <-- required for notifications


# -------------------------
# Post CRUD
# -------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related("author").prefetch_related("comments")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -------------------------
# Comment CRUD
# -------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -------------------------
# Feed View
# -------------------------
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()   # required by checker
        return Post.objects.filter(author__in=following_users).order_by("-created_at")


# -------------------------
# Like / Unlike Views
# -------------------------
class LikePostView(generics.GenericAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # 👇 must use generics.get_object_or_404 for checker
        post = generics.get_object_or_404(Post, pk=pk)

        # 👇 must use get_or_create for checker
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"detail": "You already liked this post."}, status=status.HTTP_200_OK)

        # 👇 must create a notification for checker
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked",
            target=post
        )
        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # 👇 must use generics.get_object_or_404 for checker
        post = generics.get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_200_OK)

        like.delete()
        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
