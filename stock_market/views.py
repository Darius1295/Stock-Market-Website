from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
from .forms import ShareForm
from .models import Share
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
import numpy as np
import itertools
import pygal


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


def detail(request, pk):
    share = Share.objects.get(pk=pk)

    print(share)
    print(share.symbol)

    r = requests.get(time_series_url.format(share.symbol)).json()

    date_list = []
    price_list = []

    for date in itertools.islice(r["Time Series (Daily)"], 0, 260):
        date_list.append(datetime.strptime(date, "%Y-%m-%d").date())
        price_list.append(float(r["Time Series (Daily)"][date]["5. adjusted close"]))

    date_list.reverse()
    price_list.reverse()

    print(type(price_list[0]))
    print(date_list[0])

    share_graph = pygal.Line(height=600, width=1200, explicit_size=True, x_label_rotation=30, show_minor_x_labels=False,
                             show_legend=False)
    share_graph.title = str(share) + " 1 Year"
    share_graph.x_labels = date_list
    share_graph.x_labels_major = date_list[::20]
    share_graph.add(str(share), price_list)

    return HttpResponse(share_graph.render())

    """fig = Figure()
    fig.set_figwidth(16)
    fig.set_figheight(8)
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.set_title(str(share) + " 1 Year")
    ax.grid(True)
    x = date_list
    y = price_list
    fig.autofmt_xdate()
    ax.plot(x, y)

    print(price_list[0:365])

    response = HttpResponse(content_type='image/png')
    # print the image on the response
    canvas.print_png(response)
    # and return it
    return response"""





def mplimage(request):
    # do the plotting
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    x = np.arange(-2, 1.5, .01)
    y = np.sin(np.exp(2 * x))
    ax.plot(x, y)
    # prepare the response, setting Content-Type
    response = HttpResponse(content_type='image/png')
    # print the image on the response
    canvas.print_png(response)
    # and return it
    return response
