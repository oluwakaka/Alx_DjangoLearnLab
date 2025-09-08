from django.urls import path
from .views import NotificationListView, NotificationMarkReadView

urlpatterns = [
    path("", NotificationListView.as_view(), name="notifications"),
    path("mark-read/<int:pk>/", NotificationMarkReadView.as_view(), name="notification-mark-read"),
]
