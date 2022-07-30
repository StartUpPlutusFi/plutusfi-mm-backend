from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth.serializers import *


# Create your views here.


class RegisterUserView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def auth_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token = self.auth_user(serializer.instance)

        return Response(dict(serializer.data) | token, status=status.HTTP_201_CREATED)


class GetProfileInfoView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            ProfileInforSerializer(request.user.profile).data, status=status.HTTP_200_OK
        )


class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileUpdateSerializer
    http_method_names = ("put",)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.data)
        if "picture" in request.data:
            data = data | {"picture": request.data.get("picture")}

        updated = serializer.update(request.user, data)
        return Response(ProfileInforSerializer(updated).data, status=status.HTTP_200_OK)
