from api.models import Result, Account
from rest_framework import serializers


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ("name", )

