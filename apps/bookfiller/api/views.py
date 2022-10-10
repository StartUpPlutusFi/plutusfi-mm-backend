from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.exchange.helper.helper import status_code
from rest_framework import status

from apps.bookfiller.serializers import *
from apps.bookfiller.models.models import *

from apps.exchange.services.bigone.bigone_core import *
from apps.exchange.services.biconomy.biconomy_core import *

import time


class BookFillerList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializer

    def get_queryset(self):
        result = BookFiller.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BookFillerAdd(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializer

    def post(self, request, *args, **kwargs):

        try:
            res = dict(request.data)
            insert_data = res | {
                "user_id": request.user.id,
                "api_key_id": ApiKeys.objects.filter(id=res['api_key_id'], user_id=request.user.id).values('id').first()['id']
            }

            serializer = BookFillerSerializer(data=insert_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(status_code(5, f"Data is invalid {serializer}"))

        except Exception as err:
            return Response(
                {
                    "status": "error",
                    "code": "invalid data or unauthorized api_key_id",
                    "data": str(err)
                }
            )


class BookFillerDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializer

    def get_queryset(self):
        result = BookFiller.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        )
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BookFillerDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        result = BookFiller.objects.filter(
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


class BookFillerUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializerUpdate
    http_method_names = ("put",)

    def get_queryset(self):
        result = BookFiller.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def put(self, request, *args, **kwargs):
        try:
            res = dict(request.data)
            insert_data = res | {
                "user_id": request.user.id,
                "api_key_id": ApiKeys.objects.filter(id=res['api_key_id'], user_id=request.user.id).values('id').first()['id'],
            }
            serializer = self.serializer_class(data=insert_data)
            serializer.is_valid(raise_exception=True)
            data = serializer.update(self.get_queryset(), validation_data=serializer.data)
            return Response(BookFillerSerializer(data).data)

        except Exception as err:

            return Response(
                {
                    "status": "error",
                    "msg": "invalid data or unauthorized api_key_id",
                    "code": str(err)
                }
            )


class BookFillerStatus(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializerStatus
    http_method_names = ("get",)

    def get_queryset(self):
        data = BookFiller.objects.filter(
            id=self.kwargs.get("pk"), user=self.request.user
        )
        return data

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BookFillerCtrl(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializerStatusUpdate
    http_method_names = ("get",)

    def get_queryset(self):
        result = BookFiller.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def get(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            bot_ex = data.api_key.exchange.name
            # op_result = None

            if data.status == "STOP":

                if "biconomy" == bot_ex:
                    op_result = biconomy_init_bookbot(data)
                elif "bigone" == bot_ex:
                    op_result = bigone_init_bookbot(data)
                else:
                    op_result = {
                        "status": "error",
                        "code": "Exchange not found"
                    }

                BookFiller.objects.filter(
                    id=self.kwargs.get("pk"), user=request.user
                ).update(status="START")

                return Response({
                    "status": "success",
                    "op": op_result,
                    "bot": bot_ex,
                })

            else:

                # Cancel all orders
                if "biconomy" == bot_ex:
                    exit_codes = biconomy_cancel_all_orders(data)
                elif "bigone" == bot_ex:
                    exit_codes = bigone_cancel_all_orders(data)
                else:
                    exit_codes = []

                BookFiller.objects.filter(
                    id=self.kwargs.get("pk"), user=request.user
                ).update(status="STOP")

            return Response({
                "status": "success",
                "exit_codes": exit_codes,
            })

        except Exception as e:
            return Response({"status": "error", "code": str(e)})
