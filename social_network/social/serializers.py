from rest_framework import serializers
from .models import CustomUser, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model, used for user sign-up.
    Only requires email and password fields.
    """

    class Meta:
        model = CustomUser
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class UserSearchSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model, used for searching users.
    """

    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "username", "first_name", "last_name"]


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for FriendRequest model, handles creation of friend requests.
    """

    class Meta:
        model = FriendRequest
        fields = ["id", "from_user", "to_user", "status", "created_at"]
        read_only_fields = ["status", "created_at"]

    def create(self, validated_data):
        """
        Create a new friend request.

        Validates if from_user is not the same as to_user,
        and if there isn't already a pending friend request between the users.
        """
        from_user = validated_data["from_user"]
        to_user = validated_data["to_user"]

        # Check if from_user is trying to send request to themselves
        if from_user == to_user:
            raise serializers.ValidationError(
                "You cannot send a friend request to yourself."
            )

        # Check if a request already exists
        if FriendRequest.objects.filter(
            from_user=from_user, to_user=to_user, status="pending"
        ).exists():
            raise serializers.ValidationError("A friend request is already pending.")

        return FriendRequest.objects.create(from_user=from_user, to_user=to_user)
