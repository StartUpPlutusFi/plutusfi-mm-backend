import django.db.utils
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orderLimit.models.models import *
from apps.orderLimit.serializers import *
from apps.exchange.services.biconomy.biconomy_core import *
from apps.exchange.services.bigone.bigone_core import *


class OrderLimitList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderLimitSerializer

    def get_queryset(self):
        result = OrderLimit.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderLimitAdd(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderLimitSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj: OrderLimit = serializer.save()
            return Response(OrderLimitSerializerResponse(obj).data, 201)
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


class OrderLimitDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderLimitSerializer

    def get_queryset(self):
        result = OrderLimit.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        )
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderLimitDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        result = OrderLimit.objects.filter(
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


class OrderLimitUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderLimitSerializerUpdate
    http_method_names = ("put",)

    def get_queryset(self):
        result = OrderLimit.objects.filter(
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
            return Response(OrderLimitSerializer(data).data)

        except Exception as err:
            erros = {"error": True, "errors": {}}
            for e in err.args[0].items():
                erros["errors"][e[0]] = e[1][0]

            return Response(erros, 500)


class OrderLimitStatus(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderLimitSerializerStatus
    http_method_names = ("get",)

    def get_queryset(self):
        data = OrderLimit.objects.filter(
            id=self.kwargs.get("pk"), user=self.request.user
        )
        return data

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderLimitCtrl(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderLimitSerializerStatusUpdate
    http_method_names = ("post",)

    def get_queryset(self):
        result = OrderLimit.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def post(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            order_limit_ex = data.api_key.exchange.name
            set_status = self.request.data["status"]

            if set_status == "start":

                if "biconomy" == order_limit_ex:
                    op_result = biconomy_order_limit_open(data)
                elif "bigone" == order_limit_ex:
                    return Response({"status": "unavailable"})
                else:
                    op_result = {"status": "error", "code": "Exchange not found"}

                OrderLimit.objects.filter(
                    id=self.kwargs.get("pk"), user=request.user
                ).update(status="START")

                return Response(
                    {
                        "status": "success",
                        "result": {
                            "op": op_result,
                            "bot": order_limit_ex,
                        },
                    }
                )

            else:

                # Cancel all orders by order limit cfg
                if "biconomy" == order_limit_ex:
                    exit_codes = biconomy_order_limit_close(data)
                elif "bigone" == order_limit_ex:
                    return Response({"status": "unavailable"})
                else:
                    exit_codes = []

                OrderLimit.objects.filter(
                    id=self.kwargs.get("pk"), user=request.user
                ).update(status="STOP")

            return Response(
                {
                    "status": "success",
                    "result": {"op": exit_codes},
                }
            )

        except Exception as err:
            return Response({"status": "error", "code": str(err)})
