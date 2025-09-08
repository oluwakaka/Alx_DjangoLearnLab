from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by("-timestamp")


class NotificationMarkReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        notif = self.get_object()
        if notif.recipient != request.user:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        notif.unread = False
        notif.save()
        return Response(NotificationSerializer(notif).data)
