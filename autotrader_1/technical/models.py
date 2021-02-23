from django.db import models

# Create your models here.

# 売買を記録するモデル


class SignalEvents(models.Model):
    time = models.DateTimeField(null=False, primary_key=True)
    product_code = models.CharField(default="BTC_JPY", max_length=15)
    side = models.CharField(max_length=10)
    price = models.FloatField()
    size = models.FloatField()

    def __str__(self):
        return f"{self.time}:{self.product_code}:{self.side}:price={self.price},size={self.size}"

# tickerを記録するモデル


class Candle_1hBTC_JPY(models.Model):
    time = models.DateTimeField(primary_key=True)
    product_code = models.CharField(default="BTC_JPY", max_length=15)
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()

    def __str__(self):
        return f"duration=h,{self.time} {self.product_code} open={self.open} close={self.close} volume={self.volume}"
