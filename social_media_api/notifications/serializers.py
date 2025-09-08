from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(source="actor.username", read_only=True)
    recipient = serializers.CharField(source="recipient.username", read_only=True)
    target_content_type = serializers.CharField(source="content_type.model", read_only=True)
    target_object_id = serializers.IntegerField(source="object_id", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "actor",
            "verb",
            "target_content_type",
            "target_object_id",
            "unread",
            "timestamp",
        ]
        read_only_fields = fields
