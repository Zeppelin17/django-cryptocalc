from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Exchange
import requests, json

"""
Desc: Auxiliar function to process API Responses
in: list of responses
out: object to be returned with JsonResponse()
"""
def processAPIResponse(responseList):
    finalResponse = []
    for response in responseList:
        if response.status_code == 200:
            finalResponse.append(response.json())
        else:
            finalResponse.append({'api_error': response.status_code})
    
    return finalResponse



def krakenTicker(request):
    kraken = get_object_or_404(Exchange, name='kraken')
    responseList = []
    responseList.append(requests.get(kraken.api_endpoint + '/0/public/Ticker?pair=xbteur,etheur,dasheur,ltceur,ethxbt,dashxbt,ltcxbt'))

    apidata = processAPIResponse(responseList)
    return JsonResponse(apidata, safe=False)



def bitfinexTicker(request):
    bitfinex = get_object_or_404(Exchange, name='bitfinex')
    responseList = []
    responseList.append(requests.get(bitfinex.api_endpoint + '/v2/tickers?symbols=tBTCEUR,tETHEUR,tDSHUSD,tLTCUSD,tETHBTC,tDSHBTC,tLTCBTC'))
    
    apidata = processAPIResponse(responseList)
    return JsonResponse(apidata, safe=False)


def binanceTicker(request):
    binance = get_object_or_404(Exchange, name='binance')

    binanceCalls = []
    binanceCalls.append('/api/v3/ticker/24hr?symbol=BTCUSDT')
    binanceCalls.append('/api/v3/ticker/24hr?symbol=ETHUSDT')
    binanceCalls.append('/api/v3/ticker/24hr?symbol=DASHUSDT')
    binanceCalls.append('/api/v3/ticker/24hr?symbol=LTCUSDT')
    binanceCalls.append('/api/v3/ticker/24hr?symbol=ETHBTC')
    binanceCalls.append('/api/v3/ticker/24hr?symbol=DASHBTC')
    binanceCalls.append('/api/v3/ticker/24hr?symbol=LTCBTC')

    responseList = []
    for call in binanceCalls:
        responseList.append(requests.get(binance.api_endpoint + call))

    apidata = processAPIResponse(responseList)
    return JsonResponse(apidata, safe=False)


def hitbtcTicker(request):
    hitbtc = get_object_or_404(Exchange, name='hitbtc')

    hitbtcCalls = []
    hitbtcCalls.append('/api/2/public/ticker/BTCUSD')
    hitbtcCalls.append('/api/2/public/ticker/ETHUSD')
    hitbtcCalls.append('/api/2/public/ticker/DASHUSD')
    hitbtcCalls.append('/api/2/public/ticker/LTCUSD')
    hitbtcCalls.append('/api/2/public/ticker/ETHBTC')
    hitbtcCalls.append('/api/2/public/ticker/DASHBTC')
    hitbtcCalls.append('/api/2/public/ticker/LTCBTC')

    responseList = []
    for call in hitbtcCalls:
        responseList.append(requests.get(hitbtc.api_endpoint + call))

    apidata = processAPIResponse(responseList)
    return JsonResponse(apidata, safe=False)


def okexTicker(request):
    okex = get_object_or_404(Exchange, name='okex')

    okexCalls = []
    okexCalls.append('/api/spot/v3/instruments/BTC-USDT/ticker')
    okexCalls.append('/api/spot/v3/instruments/ETH-USDT/ticker')
    okexCalls.append('/api/spot/v3/instruments/DASH-USDT/ticker')
    okexCalls.append('/api/spot/v3/instruments/LTC-USDT/ticker')
    okexCalls.append('/api/spot/v3/instruments/ETH-BTC/ticker')
    okexCalls.append('/api/spot/v3/instruments/DASH-BTC/ticker')
    okexCalls.append('/api/spot/v3/instruments/LTC-BTC/ticker')

    responseList = []
    for call in okexCalls:
        responseList.append(requests.get(okex.api_endpoint + call))

    apidata = processAPIResponse(responseList)
    return JsonResponse(apidata, safe=False)

#Unificar formato de respuesta de diferentes API's