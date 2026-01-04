from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import KnowledgeSource, SubscriptionPlan, TaskRequest, UserSubscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "specialty",
            "preferences",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "specialty", "preferences"]

    def create(self, validated_data):
        user = User(
            username=validated_data.get("username") or validated_data["email"],
            email=validated_data["email"],
            specialty=validated_data.get("specialty", ""),
            preferences=validated_data.get("preferences", {}),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = "__all__"


class TaskRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRequest
        fields = "__all__"


class KnowledgeSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeSource
        fields = "__all__"
