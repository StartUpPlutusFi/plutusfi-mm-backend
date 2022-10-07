# Create your views here.
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exchange.serializers import *
from apps.exchange.helper.helper import status_code
from apps.exchange.models.models import *
from drf_yasg.utils import swagger_auto_schema


# ----------------------------------------------------- #
class ExchangeList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExchangeSerializer

    def get_queryset(self):
        result = Exchange.objects.all()
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ExchangeAdd(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExchangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = ExchangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status_code(2))


class ExchangeDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExchangeSerializer

    def get_queryset(self):
        result = Exchange.objects.filter(id=self.kwargs.get("pk"))
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ExchangeDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        result = Exchange.objects.filter(id=self.kwargs.get("pk"))
        return result

    @swagger_auto_schema(operation_description="partial_update description override", responses={404: 'slug not found'})
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


class ExchangeUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExchangeSerializerUpdate
    http_method_names = ("put",)

    def get_queryset(self):
        result = Exchange.objects.filter(id=self.kwargs.get("pk")).first()
        return result

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(self.get_queryset(), validation_data=serializer.data)
        return Response(ExchangeSerializer(data).data)


# ----------------------------------------------------- #
# ApiKey Views
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
    serializer_class = ApiKeySerializer

    def post(self, request, *args, **kwargs):
        insert_data = dict(request.data) | {
            "user": request.user.id,
        }

        serializer = ApiKeySerializer(data=insert_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response({
            "status": "error",
            "code": "Invalid data",
            "data": serializer.data
        })


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
    serializer_class = ApiKeySerializerDetail

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
    http_method_names = ("put",)

    def get_queryset(self):
        result = ApiKeys.objects.filter(
            id=self.kwargs.get("pk"), user=self.request.user
        ).first()
        return result

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(self.get_queryset(), validation_data=serializer.data)
        return Response(ApiKeySerializer(data).data)
