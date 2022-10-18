# Create your views here.
import json

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.exchange.helper.helper import status_code
from rest_framework import status

from apps.exchange.services.bigone.bigone_core import *
from apps.exchange.services.biconomy.biconomy_core import *
from apps.geneses.serializers import *
from apps.geneses.models.models import *

logger = logging.getLogger('geneses')


class GenesesList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenesesSerializer

    def get_queryset(self):
        result = Geneses.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )
        return result

    def get(self, request, *args, **kwargs):
        try:
            logging.info("normal process")
            return self.list(request, *args, **kwargs)

        except Exception as err:
            logging.critical(str(err))
            return Response({
                "status": "error",
                "code": str(err),
            },  status=status.HTTP_400_BAD_REQUEST)


class GenesesAdd(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenesesSerializer

    def post(self, request, *args, **kwargs):
        try:
            res = dict(request.data)
            insert_data = res | {
                "user_id": request.user.id,
                "api_key_id": ApiKeys.objects.filter(id=res['api_key_id'], user_id=request.user.id).values('id').first()['id']
            }

            serializer = GenesesSerializer(data=insert_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response( {
                    "status": "error",
                    "msg": serializer,
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            return Response(
                {
                    "status": "error",
                    "msg": "invalid data or unauthorized api_key_id",
                    "code": str(err)
                }, status=status.HTTP_400_BAD_REQUEST
            )


class GenesesDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenesesSerializer

    def get_queryset(self):
        result = Geneses.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        )
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GenesesDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        result = Geneses.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
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


class GenesesUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenesesSerializerUpdate
    http_method_names = ("put",)

    def get_queryset(self):
        result = Geneses.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def put(self, request, *args, **kwargs):
        try:
            res = dict(request.data)
            insert_data = res | {
                "user_id": request.user.id,
                "api_key_id": ApiKeys.objects.filter(id=res['api_key_id'], user_id=request.user.id).values('id').first()['id']
            }
            serializer = self.serializer_class(data=insert_data)
            serializer.is_valid(raise_exception=True)
            data = serializer.update(self.get_queryset(), validation_data=serializer.data)
            return Response(GenesesSerializer(data).data)

        except Exception as err:

            return Response(
                {
                    "status": "error",
                    "msg": "invalid data or unauthorized api_key_id",
                    "code": str(err)
                },
            )


class GenesesStatus(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenesesSerializerStatus
    http_method_names = ("get",)

    def get_queryset(self):
        data = Geneses.objects.filter(
            id=self.kwargs.get("pk"), user=self.request.user
        )
        return data

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GenesesCtrl(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenesesSerializerStatusUpdate
    http_method_names = ("get",)

    def get_queryset(self):
        result = Geneses.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def get(self, request, *args, **kwargs):

        try:
            geneses_bot = self.get_queryset()
            bot_ex = geneses_bot.api_key.exchange.name
            # op_result = None

            if geneses_bot.status == "STOP":

                if "biconomy" == bot_ex:
                    op_result = biconomy_market_creator_open(geneses_bot)
                elif "bigone" == bot_ex:
                    op_result = bigone_market_creator_open(geneses_bot)
                else:
                    op_result = {
                        "status": "error",
                        "code": "Exchange not found"
                    }

                Geneses.objects.filter(
                    id=self.kwargs.get("pk"), user=request.user
                ).update(status="START")

                return Response({
                    "status": "pass",
                    "op": op_result,
                    "bot": bot_ex,
                }, status=status.HTTP_202_ACCEPTED)

            else:

                # Cancel all orders
                if "biconomy" == bot_ex:
                    exit_codes = biconomy_market_creator_close(geneses_bot)
                elif "bigone" == bot_ex:
                    exit_codes = bigone_market_creator_close(geneses_bot)
                else:
                    exit_codes = []

                Geneses.objects.filter(
                    id=self.kwargs.get("pk"), user=request.user
                ).update(status="STOP")

                return Response({
                    "status": "success",
                    "op": exit_codes,
                    "bot": bot_ex,
                }, status=status.HTTP_202_ACCEPTED)

        except Exception as err:

            return Response({
                "status": "fail",
                "code": str(err),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
