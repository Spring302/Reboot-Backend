from rest_framework import serializers
from rec.models import *


class ApartmentsPriceSerializer(serializers.ModelSerializer):
    price_info = serializers.StringRelatedField(many=True)

    class Meta:
        model = Apartments
        fields = ["id", "name", "price_info"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

class ApartmentsSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    class Meta:
        model = Apartments
        fields = ["id", "name", "users"]


class PriceInfoSerializer(serializers.ModelSerializer):
    apart = ApartmentsSerializer(read_only=True)

    class Meta:
        model = PriceInfo
        fields = ["id", "apart", "transaction_style", "date", "price"]
