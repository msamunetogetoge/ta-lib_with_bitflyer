import datetime
import os
import sys

import pybitflyer

from src import key

from technical.models import *


class Ticker():
    """Ticker を取得するクラス。
    """

    def __init__(self, api_key=None, api_secret=None, code="BTC_JPY"):
        self.api = pybitflyer.API(api_key, api_secret)
        self.product_code = code
        self.ticker = self.api.ticker(product_code=self.product_code)

    def DateTime(self, time=None):
        """[summary] create datetime.datetime object from ticker or str object

        Args:
            time ([type], optional): [description]. str or datetime.datetime object

        Returns:
            [type]datetime.datetime: [description]format='%Y-%m-%dT%H:%M:%S'
        """
        timeformat = "%Y-%m-%dT%H:%M:%S"
        if time is None:
            date = self.ticker["timestamp"][:19]
            date = datetime.datetime.strptime(date, timeformat)
            return date
        elif isinstance(time, str):
            date = time[:19]
            date = datetime.datetime.strptime(date, timeformat)
            return date

        elif isinstance(time, datetime.datetime):
            timeformat = "%Y-%m-%dT%H:%M:%S"
            date = datetime.datetime.strptime(
                time.strftime(timeformat), timeformat)
            # date = time
        else:
            print("time type is must be str or datetime.datetime ")

        return date

    def TruncateDateTime(self, duration="h", time=None):
        """[summary] create trucated datetime like datetime.datetime(year,month,hour)

        Args:
            duration ([type]): [description]
            time ([type], optional): [description]. Defaults to None.

        Returns:
            [type]datetime.datetime: [description] duration='h'→datetime.datetime(year,month,hour)
        """
        if time is None:
            date = self.DateTime()
        else:
            date = self.DateTime(time)

        timeformat = "%Y-%m-%dT%H"
        date = datetime.datetime.strptime(
            date.strftime(timeformat), timeformat)

        return date

    def GetMidPrice(self):
        """GetMidPrice from ticker

        Returns:
            float: (BestBid +BestAsk) /2
        """
        return (self.ticker["best_bid"] + self.ticker["best_ask"]) / 2


class Candle(Ticker):
    """[summary]tickerからcandleを作ったり、モデルに保存したりする。

    Args:
        Ticker ([type]): [description] ticker class
    """

    def __init__(self, api_key, api_secret, code="BTC_JPY"):
        super().__init__(api_key=api_key, api_secret=api_secret, code=code)

    def GetCandle(self, duration="h", time=None):
        """[summary] Get or create django.db.models objects.
            Filtering time=now(time=None) or given time, then, if  'ticker' was exits in models(Candle_1s, etc...), get it.
            If objects was not exists, create time=given time(or now) prices = self.MidPrice().

        Args:
            duration ([type]str in ['s, 'm', 'h']) ): [description] s, m or h decide which models choosen.

        Returns:
            [type]chart.models.Candle_1s, 1m, 1h: [description] data which is time = self.ticker['timestamp']
        """
        model = "Candle_1" + duration + self.product_code
        candle = eval(model)
        date = self.TruncateDateTime(duration=duration, time=time)
        if not candle.objects.filter(time=date, product_code=self.product_code).exists():
            price = self.GetMidPrice()
            candle = candle(
                time=date,
                product_code=self.product_code,
                open=price,
                close=price,
                high=price,
                low=price,
                volume=self.ticker["volume"])
            candle.save()
            return candle
        else:
            try:
                c = candle.objects.get(time=date, product_code=self.product_code)
            except Exception as e:
                print(e)
                print("models.get method is failed.")
                c = candle.objects.filter(time=date, product_code=self.product_code).first()

            return c

    def CreateCandleWithDuration(self, duration="h", time=None):
        """[summary] get candle from self.GetCandle. then update candle params and save.

        Args:
            duration ([type]): [description]
        """
        current_candle = self.GetCandle(duration=duration, time=time)
        price = self.GetMidPrice()

        current_candle.open = current_candle.open
        current_candle.close = price
        if current_candle.high <= price:
            current_candle.high = price
        elif current_candle.low >= price:
            current_candle.low = price
        current_candle.volume += self.ticker["volume"]
        current_candle.save()

    def GetAllCandle(self, duration="h"):
        """[summary]Get django.db.models object from duration. if duration='h', this funcution returns chart.models.Candle_1hBTC_JPY.
        Args:
            duration ([type] str ): [description] h means Candle_1hBTC_JPY

        Returns:
            [type]: [description] django.db.models from chart.models
        """
        model = "Candle_1" + duration + self.product_code
        model = eval(model)
        return model
