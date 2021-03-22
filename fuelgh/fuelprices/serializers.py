from rest_framework import serializers
from fuelprices.models import Omc
from fuelprices.models import FuelStation
from django.contrib.auth.models import User


class OmcSerializer(serializers.ModelSerializer):

    class Meta:
        model = Omc
        fields = ('id', 'name', 'diesel_price', 'petrol_price')

    def create(self, validated_data):
        return Omc.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.diesel_price = validated_data.get('diesel_price', instance.name)
        instance.petrol_price = validated_data.get('petrol_price', instance.name)
        instance.save()
        return instance


class FuelStationSerializer(serializers.ModelSerializer):
    omc = serializers.PrimaryKeyRelatedField(queryset=Omc.objects.all())
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = FuelStation
        fields = ('id', 'describer_string', 'longitude', 'latitude', 'region', 'locality', 'omc', 'uploader')

    def create(self, validated_data):
        #
        return FuelStation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('describer_string', instance.name)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

    def create(self, validated_data):
        return User.objects.create(**validated_data)
