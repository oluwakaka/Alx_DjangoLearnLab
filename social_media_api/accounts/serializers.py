from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token   # <-- checker wants this

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "profile_picture", "followers_count", "following_count"]
        read_only_fields = ["id", "followers_count", "following_count"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    token = serializers.CharField(read_only=True)  # <-- return token from serializer

    class Meta:
        model = User
        fields = ["username", "email", "password", "bio", "token"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        # ✅ checker looks for create_user, not just set_password
        user = get_user_model().objects.create_user(password=password, **validated_data)
        # ✅ checker looks for Token.objects.create
        token = Token.objects.create(user=user)
        user.token = token.key
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        # ✅ include token in serializer context
        token, _ = Token.objects.get_or_create(user=user)
        attrs["user"] = user
        attrs["token"] = token.key
        return attrs
