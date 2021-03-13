# Python Imports
from threading import Thread

# DRF imports
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import (
    FileUploadParser,
    JSONParser,
    MultiPartParser
)
from rest_framework.response import Response

# Django Imports
from django.db.models import Sum, Count

# Local Imports
from bank.services import dump_to_db
from bank.serializers import (
    BankSerializer,
    UploadBankFile,
    IFSCSerializer
)
from bank.models import Ifsc, IfscSearchTrack


class BankViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Ifsc.objects.all()
    serializer_class = BankSerializer
    parser_classes = [JSONParser, MultiPartParser]

    @action(methods=['post'], detail=False)
    def load_to_db(self, request, format=None):
        """
        :param request: Request from the user
        :param format: ---
        :return: Dump the data from DB
        """
        file = request.FILES.get('file')
        # Initilization of thread
        thead = Thread(target=dump_to_db, args=[file])
        thead.start()
        return Response({"message": "We are inserting data into the DB"}, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False)
    def bank_details(self, request, format=None):
        """
        :param request: Request from the user
        :param format: ---
        :return: Return the bank details if IFSC code exits else 404 status
        """
        ifsc = request.GET.get("ifsc_code")
        try:
            ifsc_obj = Ifsc.objects.get(ifsc=ifsc)
        except Ifsc.DoesNotExist:
            return Response({"message": "Unable to find the ifsc code"}, status=status.HTTP_404_NOT_FOUND)
        IfscSearchTrack.objects.create(ifsc=ifsc_obj)
        return Response({"message": "Search record inserted"}, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False)
    def leader_board_detail(self, request, format=None):
        """
        :param request: Requset from the user
        :param format: ---
        :return: Returns the leaderboard data
        """
        data = Ifsc.objects.all().values('bank_name').annotate(count_val=Count('bank_name')).order_by('-count_val')[:10]
        return Response({"data": data}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def search_track_details(self, request, format=None):
        """
        :param request: Request from the user
        :param format: ---
        :return: return the search stats
        """
        data = IfscSearchTrack.objects.all().values('ifsc__bank_name').annotate(
            count_val=Count('ifsc__bank_name')).order_by('-count_val')[:10]
        return Response({"data": data}, status=status.HTTP_200_OK)
