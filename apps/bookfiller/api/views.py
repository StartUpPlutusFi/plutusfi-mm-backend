import django.db.utils
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.bookfiller.serializers import *
from apps.exchange.services.biconomy.biconomy_core import *
from apps.exchange.services.bigone.bigone_core import *


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj: BookFiller = serializer.save()
            return Response(BookFillerSerializerResponse(obj).data, 201)
        except django.db.utils.IntegrityError as err:
            if "FOREIGN KEY constraint failed" in err.args:
                return Response(
                    {
                        "error": True,
                        "message": "ID entered is invalid, please check and try again.",
                    },
                    500,
                )
            return Response(
                {"error": True, "message": f"An error occurred: {err.args}"}
            )
        except Exception as err:
            return Response(
                {"error": True, "message": f"An error occurred: {err.args}"}
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
                return Response({"status": "done"}, 204)
            else:
                return Response(
                    {"status": "data not found"}, status=status.HTTP_404_NOT_FOUND
                )

        except Exception as err:
            return Response(
                {"status": "data not found"}, status=status.HTTP_404_NOT_FOUND
            )


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

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.update(
                self.get_queryset(), validation_data=serializer.data
            )
            return Response(BookFillerSerializer(data).data)

        except Exception as err:
            erros = {"error": True, "errors": {}}
            for e in err.args[0].items():
                erros["errors"][e[0]] = e[1][0]

            return Response(erros, 500)


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


class BookFillerCancelCode(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializerStatus
    http_method_names = ("get",)

    def get_queryset(self):
        data = CancelOrderBookBot.objects.filter(
            bot_id=self.kwargs.get("pk"), bot__user=self.request.user
        )
        return data

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        return Response(
            data.values()
        )


class BookFillerCtrl(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializerStatusUpdate
    http_method_names = ("post",)

    def get_queryset(self):
        result = BookFiller.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def post(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            bot_ex = data.api_key.exchange.name
            set_status = self.request.data.get("status")

            if set_status == "start":

                if "biconomy" == bot_ex:
                    op_result = biconomy_init_bookbot(data)
                elif "bigone" == bot_ex:
                    op_result = bigone_init_bookbot(data)
                else:
                    op_result = {"status": "error", "code": "Exchange not found"}

                BookFiller.objects.filter(
                    id=self.kwargs.get("pk"), user=request.user
                ).update(status="START")

                return Response(
                    {
                        "status": "success",
                        "result": {
                            "exchange_operation_result": op_result,
                            "bot_id": data.id,
                        }
                    }
                )

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

            return Response(
                {
                    "status": "success",
                    "result": {
                        "exchange_operation_result": exit_codes,
                        "bot_id": data.id,
                    },
                }
            )

        except Exception as e:
            return Response({"status": "error", "code": str(e)})
