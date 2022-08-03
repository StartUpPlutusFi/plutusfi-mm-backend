from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.account.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
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


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        fields = ("id",)


class UserRelatedField(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )


class ProfileInforSerializer(serializers.ModelSerializer):
    user = UserRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    picture = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            if k == "picture":
                setattr(instance.profile, k, v)
                instance.profile.save()
            else:
                setattr(instance, k, v)

        instance.save()
        return instance.profile
