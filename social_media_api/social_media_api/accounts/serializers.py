from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Count
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'bio', 'profile_picture', 'followers_count', 'following_count']
        read_only_fields = ['id', 'followers_count', 'following_count']


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'bio']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    # allow username OR email via same field
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')
        user = None

        # try username first
        try:
            user = User.objects.get(username=login)
        except User.DoesNotExist:
            # try email
            try:
                user = User.objects.get(email__iexact=login)
            except User.DoesNotExist:
                pass

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials.")

        attrs['user'] = user
        return attrs
