"""/**
 * URL config file for exchange app
 *
 * @summary URL config file for exchange app
 * @author Zeppelin17 <elzeppelin17@gmail.com>
 *
 * Created at     : 2020-04-01 06:44:25 
 * Last modified  : 2020-04-01 06:44:43
 */"""

from django.urls import path
from . import views

urlpatterns = [
    path('kraken/ticker/', views.krakenTicker, name='krakenticker'),
    path('bitfinex/ticker/', views.bitfinexTicker, name='bitfinexticker'),
    path('binance/ticker/', views.binanceTicker, name='binanceticker'),
    path('hitbtc/ticker/', views.hitbtcTicker, name='hitbtcticker'),
    path('okex/ticker/', views.okexTicker, name='okexticker'),
    #path('blockchain/ticker/', views.blockchainTicker, name='blockchainticker'),
]