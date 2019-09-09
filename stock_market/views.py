from django.shortcuts import render
import requests
import os

# Create your views here.

def index(request):

    share_url = os.environ.get("SHARE_URL")
    symbol = 'MSFT'
    r = requests.get(share_url.format(symbol)).json()

    msft_open = r["Global Quote"]["02. open"]
    msft_high = r["Global Quote"]["03. high"]
    msft_low = r["Global Quote"]["04. low"]
    msft_price = r["Global Quote"]["05. price"]
    msft_volume = r["Global Quote"]["06. volume"]
    msft_prev_close = r["Global Quote"]["08. previous close"]

    context = {'open': msft_open, 'high': msft_high, 'low': msft_low,
               'price': msft_price, 'volume': msft_volume, 'prev_close': msft_prev_close}

    return render(request, 'stock_market/index.html', context)
