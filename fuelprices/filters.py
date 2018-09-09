import django_filters
from fuelprices.models import FuelStation

class FuelStationFilter(django_filters.FilterSet):
	omc = django_filters.CharFilter(name="omc__name")

	class Meta:
		model = FuelStation
		fields = ['omc']