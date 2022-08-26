from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.exchange.helper.helper import status_code
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
        insert_data = dict(request.data) | {
            "user_id": request.user.id,
        }

        serializer = BookFillerSerializer(data=insert_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(status_code(2))


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
            return self.destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                status_code(
                    5,
                    "Cannot delete a parent row, check foreign key constraint or if the object exist",
                )
            )


class BookFillerUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializerUpdate

    def get_queryset(self):
        result = BookFiller.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(self.get_queryset(), validation_data=serializer.data)
        return Response(BookFillerSerializer(data).data)


class BookFillerStatus(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializerStatus

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

    def get_queryset(self):
        result = BookFiller.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def get(self, request, *args, **kwargs):
        if True:
            data = self.get_queryset()
            bot_ex = data.api_key.exchange.name
            op_result = None

            if data.status == "STOP":

                if "biconomy" == bot_ex:
                    op_result = biconomy_init_bookbot(data)
                    # op_result = {"pass": True}
                elif "bigone" == bot_ex:
                    # op_result = bigone_init_bookbot(data)
                    pass
                else:
                    pass

                BookFiller.objects.filter(
                    id=self.kwargs.get("pk"), user=request.user
                ).update(status="START")

                return Response({
                    "status": "success",
                    "op": op_result,
                })

            else:

                # Cancel all orders
                exit_codes = biconomy_cancel_all_orders(data)

                BookFiller.objects.filter(
                    id=self.kwargs.get("pk"), user=request.user
                ).update(status="STOP")

            return Response({
                "status": "success",
                "exit_codes": exit_codes,
            })

        # except Exception as e:
        #     return Response({"status": "error", "check": str(e)})
