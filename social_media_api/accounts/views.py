from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User as CustomUser
from .serializers import (
    LoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


# -------------------------
# Registration & Login
# -------------------------

class RegisterView(generics.CreateAPIView):
    """Register a new user"""
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            "user": UserSerializer(user, context={"request": request}).data,
            "token": serializer.data.get("token"),
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Login an existing user"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = serializer.validated_data["token"]
        return Response({
            "user": UserSerializer(user, context={"request": request}).data,
            "token": token,
        })


# -------------------------
# Profile Management
# -------------------------

class ProfileView(APIView):
    """View or update the authenticated user's profile"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user, context={"request": request}).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# -------------------------
# Follow / Unfollow System
# -------------------------

class FollowUserView(generics.GenericAPIView):
    """Follow another user"""
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, pk=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.following.filter(pk=target.pk).exists():
            return Response({"detail": f"Already following {target.username}."}, status=status.HTTP_200_OK)
        request.user.following.add(target)
        return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    """Unfollow another user"""
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, pk=user_id)
        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        if not request.user.following.filter(pk=target.pk).exists():
            return Response({"detail": f"You are not following {target.username}."}, status=status.HTTP_200_OK)
        request.user.following.remove(target)
        return Response({"detail": f"You have unfollowed {target.username}."}, status=status.HTTP_200_OK)


class FollowingListView(generics.ListAPIView):
    """List of users the authenticated user is following"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.following.all()


class FollowersListView(generics.ListAPIView):
    """List of users who follow the authenticated user"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.followers.all()
