# Create your views here.
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exchange.serializers import *
from apps.exchange.helper.crypto_utils import EncryptationTool
from apps.exchange.models.models import *
from rest_framework import status


# ----------------------------------------------------- #
class ExchangeList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExchangeSerializer

    def get_queryset(self):
        result = Exchange.objects.all().order_by(
            "-created_at"
        )
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# ----------------------------------------------------- #


class ApiKeyList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ApiKeySerializerDetail

    def get_queryset(self):
        result = ApiKeys.objects.filter(
            user=self.request.user
        ).values("id", "description", "default", "exchange_id")
        return result

    def get(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            return Response(data)
        except Exception:

            return Response({
                "status": "data id not found"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiKeyAdd(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ApiKeySerializer

    def post(self, request, *args, **kwargs):
        insert_data = dict(request.data) | {
            "user": request.user.id,
            "api_key": EncryptationTool.encrypt(request.data['api_key'].encode()),
            "api_secret": EncryptationTool.encrypt(request.data['api_secret'].encode()),
        }

        serializer = ApiKeySerializer(data=insert_data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "id": serializer.data['id'],
                "description": serializer.data['description'],
                "default":  serializer.data['default'],
                "exchange":  Exchange.objects.filter(id=serializer.data['exchange']).values("name").first()["name"],
            })

        return Response({
            "status": "error",
            "code": "Invalid data",
        })


class ApiKeyDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ApiKeySerializer

    def get_queryset(self):
        result = ApiKeys.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).values("id", "description", "default", "exchange_id").first()
        return result

    def get(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            data = data | {
                "exchange": Exchange.objects.filter(id=data['exchange_id']).values("name").first()["name"],
            }
            return Response(data)

        except Exception:

            return Response({
                "status": "data id not found"
            }, status=status.HTTP_404_NOT_FOUND)



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
            if self.destroy(request, *args, **kwargs):
                return Response({
                    "status": "done"
                })
            else:
                return Response({
                    "status": "data not found"
                }, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response({
                "status": "data not found"
            }, status=status.HTTP_404_NOT_FOUND)


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
        try:
            res = dict(request.data)
            insert_data = res | {
                "user_id": request.user.id,
            }
            serializer = self.serializer_class(data=insert_data)
            serializer.is_valid(raise_exception=True)
            data = serializer.update(self.get_queryset(), validation_data=serializer.data)
            return Response(ApiKeySerializerUpdate(data).data)

        except Exception as err:

            return Response({
                "status": "error",
                "msg": "invalid data or unauthorized api_key_id",
            }, status=status.HTTP_400_BAD_REQUEST)
