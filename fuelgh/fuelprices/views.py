# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions

from fuelprices import tasks
from fuelprices.models import FuelStation
from fuelprices.models import Omc
from fuelprices.permissions import IsOwnerOrReadOnly
from fuelprices.serializers import FuelStationSerializer
from fuelprices.serializers import OmcSerializer
from fuelprices.serializers import UserSerializer


def index(request):
    return render(request, 'fuelprices/index.html', {})


def omcs(request, fuel_type):
    if fuel_type == 'diesel':
        omc_list = Omc.objects.order_by('diesel_price')
    if fuel_type == 'petrol':
        omc_list = Omc.objects.order_by('petrol_price')
    return render(request, 'fuelprices/omcs.html', {
        'omc_list': omc_list,
    })


# User views
class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


# OMC views
class OmcList(generics.ListAPIView):
    """
    You can order by `petrol_price` and `diesel_price`
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Omc.objects.all()
    serializer_class = OmcSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ['petrol_price', 'diesel_price']

    def perform_create(self, serializer):
        serializer.save()


class OmcDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Omc.objects.all()
    serializer_class = OmcSerializer


# FuelStation views:
class FuelStationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = FuelStation.objects.all()
    serializer_class = FuelStationSerializer


class FuelStationList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = FuelStationSerializer

    def get_queryset(self):
        omc_ = self.request.query_params.get('omc', None)
        latit = self.request.query_params.get('latitude', None)
        longit = self.request.query_params.get('longitude', None)
        uploader = self.request.query_params.get('uploader', None)
        # if fuelstations become that many
        locality = self.request.query_params.get('locality', None)

        queryset = FuelStation.objects.filter(omc__name=omc_)

        queryset_uploader = FuelStation.objects.filter(uploader__username=uploader)

        queryset_uploader_omc = FuelStation.objects.filter(uploader__username=uploader, omc__name=omc_)

        if latit is None and longit is None and omc_ is None and uploader is None:
            return FuelStation.objects.all()
        if latit is None and longit is None and omc_ is not None and uploader is None:
            return queryset
        if latit is None and longit is None and omc_ is None and uploader is not None:
            return queryset_uploader
        if latit is None and longit is None and omc_ is not None and uploader is not None:
            return queryset_uploader_omc

        if locality is not None:
            queryset = FuelStation.objects.filter(omc__name=omc_, locality=locality)

        ordered_queryset = queryset.extra(
            select={'farness': 'select ((latitude-(%f)) * (latitude-(%f))) + ((longitude-(%f)) * (longitude-(%f)))'
                               % (float(latit), float(latit), float(longit), float(longit)), }, order_by=['farness', ])[
                           :5]

        return ordered_queryset

    def perform_create(self, serializer):
        serializer.save()
