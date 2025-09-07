from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, UserRegistrationSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # serializer already attached token
        data = {
            "user": UserSerializer(user, context={"request": request}).data,
            "token": serializer.data.get("token"),
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
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


class ProfileView(APIView):
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
# Follow / Unfollow Endpoints
# -------------------------

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    if request.user.following.filter(pk=target.pk).exists():
        return Response({"detail": f"Already following {target.username}."}, status=status.HTTP_200_OK)

    request.user.following.add(target)
    return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    if not request.user.following.filter(pk=target.pk).exists():
        return Response({"detail": f"You are not following {target.username}."}, status=status.HTTP_200_OK)

    request.user.following.remove(target)
    return Response({"detail": f"You have unfollowed {target.username}."}, status=status.HTTP_200_OK)


class FollowingListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.following.all()


class FollowersListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.followers.all()
