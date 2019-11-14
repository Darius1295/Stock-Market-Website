from django.urls import path
from . import views


app_name = 'stock_market'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>', views.detail, name='detail'),
    path('mplimage.png', views.mplimage, name='mplimage')
]
