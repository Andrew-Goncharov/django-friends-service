from rest_framework import fields, serializers
from .models import User, FriendshipRequest, Friend


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = ("sender", "receiver")


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ("friend_1", "friend_2")


class ProcessFriendshipRequestSerializer(serializers.Serializer):
    sender = serializers.UUIDField()
    receiver = serializers.UUIDField()
    action = serializers.CharField(max_length=6)

    def validate_action(self, value):
        """
        Check if the action is correct
        """
        if value != "accept" and value != "reject":
            raise serializers.ValidationError("The value is incorrect")
        return value
