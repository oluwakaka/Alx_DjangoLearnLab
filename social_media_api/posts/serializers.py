from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import UserSerializer  # lightweight user representation


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "comments",
            "comments_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "comments", "comments_count", "created_at", "updated_at"]

        class LikeSerializer(serializers.ModelSerializer):
            user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = ["id", "post", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
