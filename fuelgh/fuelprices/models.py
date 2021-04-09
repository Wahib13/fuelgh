import pytz
from django.db import models
from django.utils.datetime_safe import datetime


class Omc(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField()
    name = models.CharField(max_length=20, default='', db_index=True)
    diesel_price = models.DecimalField(max_digits=5, decimal_places=3, default=0, db_index=True)
    petrol_price = models.DecimalField(max_digits=5, decimal_places=3, default=0, db_index=True)

    def save(self, **kwargs):
        self.last_updated = datetime.now(pytz.utc)
        super().save()

    def __str__(self):
        return self.name


class UpdateTask(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    task_id = models.CharField(max_length=36, db_index=True)
    excel_file = models.FileField()

    def __str__(self):
        return str(self.created)


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
