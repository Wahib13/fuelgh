# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from rest_framework.authtoken.models import Token

from fuelprices.models import Omc

# Register your models here.
admin.site.register(Omc)
admin.site.register(Token)
