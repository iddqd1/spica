from rest_framework import serializers
from rest_framework import validators

from spica.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class CreateUserSerializer(serializers.ModelSerializer[User]):
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["id", "name", "email", "password", "password_confirm"]
        read_only_fields = ["id"]

        extra_kwargs = {
            "password": {"write_only": True},
        }
        validators = [
            validators.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=[
                    "email",
                ],
            ),
        ]

    def validate(self, attrs: dict):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."},
            )
        return super().validate(attrs)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
