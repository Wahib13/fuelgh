import logging
import shutil
from decimal import Decimal

import requests
from django.core.files import File
from openpyxl import load_workbook

from fuelapp.celery import app
from fuelprices.models import Omc, UpdateTask
from fuelprices.utils import fetch_latest_link

# logger_debug = logging.getLogger('debugger')
logger = logging.getLogger(__name__)


@app.task(bind=True)
def update_prices(self):
    logger.debug(self.request.id)
    url = fetch_latest_link()
    # download the file and save temporarily
    r = requests.get(url, stream=True)
    filename = '/home/app_runner/code/fuelgh/prices_latest.xlsx'
    with open(filename, 'wb') as f:
        # save the file on disk
        shutil.copyfileobj(r.raw, f)
    with open(filename, 'rb+') as f:
        UpdateTask.objects.create(task_id=self.request.id, excel_file=File(f))
    book = load_workbook(filename=filename)
    sheet_prices = book['OMCs and LPGMCs Ex-Pump Prices']
    i = 0
    while True:
        # TODO don't hardcode the expected row (i + 10). it tends to change between files
        name = sheet_prices['E' + str(i + 9)].value
        petrol_price = sheet_prices['F' + str(i + 10)].value
        diesel_price = sheet_prices['G' + str(i + 10)].value

        i = i + 1
        logger.debug(name)
        logger.debug(petrol_price)
        logger.debug(diesel_price)
        if not name:
            break
        if not petrol_price or not diesel_price:
            continue
        petrol_price = round(Decimal(petrol_price) / 100, 2)
        diesel_price = round(Decimal(diesel_price) / 100, 2)

        existing_omcs = Omc.objects.filter(name=name)
        if len(existing_omcs) > 0:
            omc_to_insert = existing_omcs[0]
            omc_to_insert.petrol_price = petrol_price
            omc_to_insert.diesel_price = diesel_price
        else:
            omc_to_insert = Omc(name=name, petrol_price=petrol_price, diesel_price=diesel_price)

        omc_to_insert.save()

