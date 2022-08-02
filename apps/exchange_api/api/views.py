# Create your views here.
from rest_framework.response import Response
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated

from apps.dashboard.db.models import *
from apps.dashboard.db.forms import *
from apps.dashboard.helper.helper import *
from apps.exchange_api.serializers import *


class ApiKeyList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ApiKeySerializer

    def get_queryset(self):
        result = ApiKeys.objects.filter(user=self.request.user)
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ApiKeyAdd(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ApiKeySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status_code(2))


class ApiKeyDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ApiKeySerializer

    def get_queryset(self):
        result = ApiKeys.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        )
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ApiKeyDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        result = ApiKeys.objects.filter(
            id=self.kwargs.get("pk"), user=self.request.user
        )
        return result

    def delete(self, request, *args, **kwargs):
        try:
            return self.destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                status_code(
                    5,
                    "Cannot delete a parent row, check foreign key constraint or if the object exist",
                )
            )


class ApiKeyUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ApiKeySerializerUpdate

    def get_queryset(self):
        result = ApiKeys.objects.filter(id=self.kwargs.get("pk")).first()
        return result

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(self.get_queryset(), validation_data=serializer.data)
        return Response(ApiKeySerializer(data).data)
