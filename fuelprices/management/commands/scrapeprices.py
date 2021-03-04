from django.core.management.base import BaseCommand

from openpyxl import load_workbook
import wget
from fuelprices.models import Omc
from decimal import Decimal
from django.contrib.auth.models import User


class OMC:
    def __init__(self, name, petrol_price, diesel_price):
        self.name = name
        self.petrol_price = petrol_price
        self.diesel_price = diesel_price


# download the necessary file from NPA website, get workbook from excel file
def download():
    print('Kindly input the url to the omc prices')
    url = str(input('>'))
    filename = wget.download(url)
    book = load_workbook(filename=filename)
    return book


# store prices from downloaded book in an array of OMCs
def scrape():
    book = download()
    sheet_prices = book['OMCs and LPGMCs Ex-Pump Prices']
    omcs = []
    for i in range(65):
        name = sheet_prices['E' + str(i + 10)].value
        petrol_price = sheet_prices['F' + str(i + 10)].value
        petrol_price = round(Decimal(petrol_price) / 100, 2)

        diesel_price = sheet_prices['G' + str(i + 10)].value
        diesel_price = round(Decimal(diesel_price) / 100, 2)

        if petrol_price > 0 and diesel_price > 0:
            omcs.append(OMC(name, petrol_price, diesel_price))
    return omcs


# import them into the DB
def importIntoDB():
    omcs = scrape()
    if (len(omcs) > 0):
        for omc in omcs:
            omc_to_insert = Omc(name=omc.name, petrol_price=omc.petrol_price, diesel_price=omc.diesel_price)
            omc_to_insert.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        # delete all old ones before importing
        Omc.objects.all().delete()
        importIntoDB()
