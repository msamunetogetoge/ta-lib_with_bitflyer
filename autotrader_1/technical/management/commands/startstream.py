from django.core.management.base import BaseCommand

import time

from technical.models import *
from technical.calc import get_data
from src import key


class Command(BaseCommand):
    """[summary] get candles ftom bitflyer api and save to DB, and save().

    Args:
        BaseCommand ([type]): [description]
    """

    def handle(self, *args, **options):
        print("Start GetCandles")
        api_key = key.api_key
        api_secret = key.api_secret
        duration = "h"
        while True:
            product_code = "BTC_JPY"
            cdl = get_data.Candle(api_key=api_key, api_secret=api_secret, code=product_code)

            cdl.CreateCandleWithDuration(duration=duration)
            model = eval("Candle_1" + duration + product_code)
            ticker = model.objects.filter(product_code=product_code).last()

            print(f"Model Data Created:{ticker}")
            time.sleep(10)
