# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from fuelprices.utils import fetch_link_to_price_sheet, fetch_link_from_download_page


class NPASheetDownloadTestCase(TestCase):
    def setUp(self):
        pass

    def testLinkFetch(self):
        home_page_link = fetch_link_to_price_sheet()
        print(f'home page link: {home_page_link}')
        download_page_link = fetch_link_from_download_page()
        print(f'download page link: {download_page_link}')
        assert home_page_link is not None
        assert home_page_link.endswith('.xlsx')
        assert download_page_link is not None
        assert download_page_link.endswith('.xlsx')
