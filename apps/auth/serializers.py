from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.account.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password1", "password2")

    def get_id(self, value):
        return self.instance.profile.id

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data, password=password)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already in use.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email fiel already in use.")
        return value

    def validate(self, value):
        if value.get("password1") != value.get("password2"):
            raise serializers.ValidationError("Password not match")
        return value
