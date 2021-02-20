from django.db import models


class Omc(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20, default='')
    diesel_price = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    petrol_price = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    owner = models.ForeignKey('auth.User', related_name='Omcs', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created',)


class FuelStation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    describer_string = models.CharField(max_length=50, default='')

    region = models.CharField(max_length=50, default='')
    locality = models.CharField(max_length=50, default='')

    omc = models.ForeignKey(Omc, on_delete=models.CASCADE)
    longitude = models.DecimalField(max_digits=25, decimal_places=20)
    latitude = models.DecimalField(max_digits=25, decimal_places=20)
    uploader = models.ForeignKey('auth.User', related_name='FuelStation', default='', on_delete=models.CASCADE)

    def __str__(self):
        return self.describer_string

    class Meta:
        ordering = ('created',)
