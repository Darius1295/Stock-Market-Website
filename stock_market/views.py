from django.shortcuts import render
import requests
import os
from .forms import ShareForm
from .models import Share

# Create your views here.

share_url = os.environ.get("SHARE_URL")
time_series_url = os.environ.get("SHARE_DAILY_TIME_SERIES_URL")

def index(request):
    form = ShareForm()

    """if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            share_obj = form.save()
            form = ShareForm"""

    my_shares = Share.objects.all()
    stock_dict = {}

    for share in my_shares:
        r = requests.get(share_url.format(share.symbol)).json()
        share_data = {
            'symbol' : r["Global Quote"]["01. symbol"],
            'open' : r["Global Quote"]["02. open"],
            'high' : r["Global Quote"]["03. high"],
            'low' : r["Global Quote"]["04. low"],
            'price' : r["Global Quote"]["05. price"],
            'volume' : r["Global Quote"]["06. volume"],
            'prev_close' : r["Global Quote"]["08. previous close"]
        }
        stock_dict[share.symbol] = share_data
        print("share_data: " + str(share_data))

    print("my_shares: " + str(my_shares))
    print("stock_dict: " + str(stock_dict))
    for key, val in stock_dict.items():
        print("share: " + str(key) + " " + str(val))

    context = {'stock_dict': stock_dict}

    return render(request, 'stock_market/index.html', context)
