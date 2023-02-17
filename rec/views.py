from urllib import request
from rec.utils.cron import Cron
from rec.models import *
from rec.serializers import *

from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import redirect

from datetime import datetime


class ApartmentsList(generics.ListCreateAPIView):
    queryset = Apartments.objects.all()
    serializer_class = ApartmentsSerializer


class ApartmentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Apartments.objects.all()
    serializer_class = ApartmentsSerializer


class PriceInfoList(generics.ListCreateAPIView):
    queryset = PriceInfo.objects.all()
    serializer_class = PriceInfoSerializer


class PriceInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PriceInfo.objects.all()
    serializer_class = PriceInfoSerializer


class TodayApartmentsList(generics.ListAPIView):
    today = datetime.today().strftime("%Y-%m-%d")
    queryset = PriceInfo.objects.filter(date=today)
    serializer_class = PriceInfoSerializer


class SearchApartmentsList(APIView):
    def get(self, request, format=None):
        apartments = Apartments.objects.all()
        apartments_serializer = ApartmentsSerializer(apartments, many=True)
        # Cron.save_price_info(apartments_serializer)
        
        response = redirect("/apart/")
        return response
