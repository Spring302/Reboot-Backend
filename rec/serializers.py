from rest_framework import serializers
from rec.models import *


class ApartmentsPriceSerializer(serializers.ModelSerializer):
    price_info = serializers.StringRelatedField(many=True)

    class Meta:
        model = Apartments
        fields = ['id', 'name', 'price_info']


class ApartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartments
        fields = ['id', 'name']


class PriceInfoSerializer(serializers.ModelSerializer):
    apart = ApartmentsSerializer(read_only=True)

    class Meta:
        model = PriceInfo
        fields = ['id', 'apart', 'date', 'price', 'per_price']
