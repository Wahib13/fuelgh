import shutil
from decimal import Decimal

import requests
from openpyxl import load_workbook

from fuelapp.celery import app
from fuelprices.models import Omc


@app.task(bind=True)
def update_prices(self):
    # TODO get the latest URL
    url = "http://www.npa.gov.gh/images/npa/documents/indicative-prices/2021/Indicative_Prices_for_1st-15th__Mar_2021.xlsx"
    # download the file and save temporarily
    r = requests.get(url, stream=True)
    filename = '/home/app_runner/prices_latest.xlsx'
    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    book = load_workbook(filename=filename)
    sheet_prices = book['OMCs and LPGMCs Ex-Pump Prices']
    # extract all into a list
    omcs = []
    # TODO detect actual full length
    number_of_omcs_in_file = 65
    for i in range(number_of_omcs_in_file):
        name = sheet_prices['E' + str(i + 10)].value
        petrol_price = sheet_prices['F' + str(i + 10)].value
        petrol_price = round(Decimal(petrol_price) / 100, 2)

        diesel_price = sheet_prices['G' + str(i + 10)].value
        diesel_price = round(Decimal(diesel_price) / 100, 2)

        if petrol_price > 0 and diesel_price > 0:
            omc_to_insert = Omc(name=name, petrol_price=petrol_price, diesel_price=diesel_price)
            omc_to_insert.save()
    # TODO store file for debugging purposes - create a table for this. keep track of every update that has been done.
