from rest_framework import serializers
from bank.models import Ifsc


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ifsc
        fields = ['id', 'bank_name', 'ifsc', 'micr_code', 'branch', 'address',
                  "std_code", "city", "district", "state"]


class UploadBankFile(serializers.Serializer):
    bank_excel = serializers.FileField()


class IFSCSerializer(serializers.Serializer):
    ifsc_code = serializers.CharField()
