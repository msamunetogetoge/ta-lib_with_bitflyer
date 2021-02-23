import pybitflyer

import key

product_code = "BTC_JPY"
api_key = key.api_key
api_secret = key.api_secret
api = pybitflyer.API()

ticker = api.ticker()
print(ticker)
