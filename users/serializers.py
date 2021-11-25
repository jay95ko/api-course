from rest_framework import serializers
from .models import User


# GET, PUT 쉽게 하는 방법
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
            "password",
            )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields=("id", "superhost", "avatar",)

    def validate_first_name(self, value):
        print(value)
        return value.upper()

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
