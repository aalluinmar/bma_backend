from rest_framework import serializers

from api.models import UserData

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = (
            "id", "username", "password", "first_name", "last_name",
            "email", "phone_number", "current_address", "city", "state",
            "country", "zip_code", "is_admin", "is_tenant", "is_active"
        )
        extra_kwargs = {"password": {"write_only": True}, "email": {"required": True}}

    def create(self, validated_data):
        user = UserData.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})
