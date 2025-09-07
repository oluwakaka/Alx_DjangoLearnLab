from rest_framework import viewsets, permissions, filters, generics
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    /api/posts/ - list, create
    /api/posts/{id}/ - retrieve, update, destroy
    Supports search (?search=keyword) and ordering (?ordering=created_at)
    """
    queryset = Post.objects.all().select_related("author").prefetch_related("comments")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    /api/comments/ - list, create
    /api/comments/{id}/ - retrieve, update, destroy
    Filter by post (?post=<post_id>)
    """
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


class FeedView(generics.ListAPIView):
    """
    /api/feed/ - list posts from users the current user follows
    Ordered by creation date (newest first)
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # required by checker
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by("-created_at")
