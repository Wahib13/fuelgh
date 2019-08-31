# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from django.http import HttpResponse, HttpResponseBadRequest
from fuelprices.models import Omc
from fuelprices.models import FuelStation
from fuelprices.serializers import OmcSerializer
from fuelprices.serializers import FuelStationSerializer
from fuelprices.serializers import UserSerializer
from fuelprices.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from django.contrib.auth.models import User
from oauth2client import client, crypt
import json
from rest_framework.authtoken.models import Token


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
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Omc.objects.all()
    serializer_class = OmcSerializer
    filter_backends = (filters.OrderingFilter,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OmcDetail(generics.RetrieveUpdateDestroyAPIView):
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
        serializer.save(uploader=self.request.user)


# create token for Google users
def googleUsers(request):
    token = request.GET.get('token', None)

    CLIENT_SECRET_FILE = '/fuelprices/client_secret_google_auth.json'
    # visit the README for instructions on how to create yours
    CLIENT_ID = '#yourclientsecret.apps.googleusercontent.com'

    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
    except crypt.AppIdentityError:
        idinfo = None

    if idinfo is not None:
        email_ = idinfo['email']
        first_name_ = idinfo['given_name']
        last_name_ = idinfo['family_name']

        try:
            user_ = User.objects.get(email=email_)
        except User.DoesNotExist:
            user_ = User.objects.create_user(username=email_, email=email_, first_name=first_name_,
                                             last_name=last_name_, password='#save#')
            token = Token.objects.create(user=user_)
        token = Token.objects.get(user=user_)
        user_data = {
            'username': user_.username,
            'email': user_.email,
            'first_name': user_.first_name,
            'last_name': user_.last_name,
            'token': token.key,
        }
        user_data_json = json.dumps(user_data)
        return HttpResponse(user_data_json, content_type='application/json')

    return HttpResponseBadRequest
