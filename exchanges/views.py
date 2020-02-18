from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Exchange
from time import sleep
import requests, json
from websocket import create_connection

"""
Desc: Helper function to process REST API Responses
in: list of responses
out: object to be returned with JsonResponse()
"""
def processRestAPIResponse(responseList):
    finalResponse = []
    for response in responseList:
        if response.status_code == 200:
            finalResponse.append(response.json())
        else:
            finalResponse.append({'api_error': response.status_code})
    
    return finalResponse


"""
Desc: Helper function to process WebSocket API Responses
in: websocket, message, method
    - websocket with already opened connection 
    - message to send to the endpoint
    - method: "send" or "receive" data
out: websocket response object in json format
"""
def processWebsocketAPIResponse(ws, method, msg=""):
    if method == "send":
        ws.send(msg)
        result = json.loads(ws.recv())
    
    if method == "receive":
        sleep(0.3)
        result = json.loads(ws.recv())
    
    return result


"""
Desc: Helper function that prepares the skeleton of the response object
in: -
out: base of response object
"""
def getResponseDictionary():
    resDict = {
        "pair": False,
        "ask": {
            "price": False,
            "volume": False,
        },
        "bid": {
            "price": False,
            "volume": False,
        },
        "volume": {
            "today": False,
            "last24": False,
        },
        "avgPrice": {
            "today": False,
            "last24": False,
        },
        "trades": {
            "today": False,
            "last24": False,
        },
        "low": {
            "today": False,
            "last24": False,
        },
        "high": {
            "today": False,
            "last24": False,
        },
        "opening": False,
    }

    return resDict

"""
Desc: Helper function that returns pair names in foormat XXX-YYY or XXX-YYYT
in: pair name
out: normalized pair name
"""
def normalizePairName(pairName):

    normalizedPairNames = [
        "DSH-USD",   #0
        "DSH-USDT",  #1
        "DSH-BTC",   #2
        "ETH-BTC",   #3
        "ETH-USD",   #4
        "ETH-USDT",  #5
        "LTC-BTC",   #6
        "LTC-USD",   #7
        "LTC-USDT",  #8
        "BTC-USD",   #9
        "BTC-USDT",  #10
    ] 

    if pairName == "DASHUSD": return normalizedPairNames[0]
    if pairName == "DASHXBT": return normalizedPairNames[2]
    if pairName == "XETHXXBT": return normalizedPairNames[3]
    if pairName == "XETHZUSD": return normalizedPairNames[4]
    if pairName == "XLTCXXBT": return normalizedPairNames[6]
    if pairName == "XLTCZUSD": return normalizedPairNames[7]
    if pairName == "XXBTZUSD": return normalizedPairNames[9]

    if pairName == "tBTCUSD": return normalizedPairNames[9]
    if pairName == "tETHUSD": return normalizedPairNames[4]
    if pairName == "tDSHUSD": return normalizedPairNames[0]
    if pairName == "tLTCUSD": return normalizedPairNames[7]
    if pairName == "tETHBTC": return normalizedPairNames[3]
    if pairName == "tDSHBTC": return normalizedPairNames[2]
    if pairName == "tLTCBTC": return normalizedPairNames[6]

    if pairName == "BTCUSDT": return normalizedPairNames[10]
    if pairName == "ETHUSDT": return normalizedPairNames[5]
    if pairName == "DASHUSDT": return normalizedPairNames[1]
    if pairName == "LTCUSDT": return normalizedPairNames[8]
    if pairName == "ETHBTC": return normalizedPairNames[3]
    if pairName == "DASHBTC": return normalizedPairNames[2]
    if pairName == "LTCBTC": return normalizedPairNames[6]

    if pairName == "BTCUSD": return normalizedPairNames[9]
    if pairName == "ETHUSD": return normalizedPairNames[4]
    if pairName == "LTCUSD": return normalizedPairNames[7]

    if pairName == "BTC-USDT": return normalizedPairNames[10]
    if pairName == "ETH-USDT": return normalizedPairNames[5]
    if pairName == "DASH-USDT": return normalizedPairNames[1]
    if pairName == "LTC-USDT": return normalizedPairNames[8]
    if pairName == "ETH-BTC": return normalizedPairNames[3]
    if pairName == "DASH-BTC": return normalizedPairNames[2]
    if pairName == "LTC-BTC": return normalizedPairNames[6]

    # if no match, return the same pair name
    return pairName
        




def krakenTicker(request):
    kraken = get_object_or_404(Exchange, name='kraken')
    responseList = []
    responseList.append(requests.get(kraken.api_endpoint + '/0/public/Ticker?pair=xbtusd,ethusd,dashusd,ltcusd,ethxbt,dashxbt,ltcxbt'))

    apidata = processRestAPIResponse(responseList)

    resList = []
    for key in apidata[0]["result"].items():
        resDict = getResponseDictionary()

        resDict["pair"] = normalizePairName(key[0])
        resDict["ask"]["price"] = apidata[0]["result"][key[0]]["a"][0]
        resDict["ask"]["volume"] = apidata[0]["result"][key[0]]["a"][1]

        resDict["bid"]["price"] = apidata[0]["result"][key[0]]["b"][0]
        resDict["bid"]["volume"] = apidata[0]["result"][key[0]]["b"][1]

        resDict["volume"]["today"] = apidata[0]["result"][key[0]]["v"][0]
        resDict["volume"]["last24"] = apidata[0]["result"][key[0]]["v"][1]

        resDict["avgPrice"]["today"] = apidata[0]["result"][key[0]]["p"][0]
        resDict["avgPrice"]["last24"] = apidata[0]["result"][key[0]]["p"][1]

        resDict["trades"]["today"] = apidata[0]["result"][key[0]]["t"][0]
        resDict["trades"]["last24"] = apidata[0]["result"][key[0]]["t"][1]

        resDict["low"]["today"] = apidata[0]["result"][key[0]]["l"][0]
        resDict["low"]["last24"] = apidata[0]["result"][key[0]]["l"][1]

        resDict["high"]["today"] = apidata[0]["result"][key[0]]["h"][0]
        resDict["high"]["last24"] = apidata[0]["result"][key[0]]["h"][1]

        resDict["opening"] = apidata[0]["result"][key[0]]["o"]


        resList.append(resDict)
    # order result by pair name
    resList = sorted(resList, key=lambda list: list["pair"])
    return JsonResponse(resList, safe=False)



def bitfinexTicker(request):
    bitfinex = get_object_or_404(Exchange, name='bitfinex')
    responseList = []
    responseList.append(requests.get(bitfinex.api_endpoint + '/v2/tickers?symbols=tBTCUSD,tETHUSD,tDSHUSD,tLTCUSD,tETHBTC,tDSHBTC,tLTCBTC'))
    
    apidata = processRestAPIResponse(responseList)

    resList = []
    for dataList in apidata[0]:
        resDict = getResponseDictionary()

        resDict["pair"] = normalizePairName(dataList[0])
        resDict["ask"]["price"] = dataList[3]
        resDict["ask"]["volume"] = dataList[4]

        resDict["bid"]["price"] = dataList[1]
        resDict["bid"]["volume"] = dataList[2]

        resDict["volume"]["last24"] = dataList[8]

        resDict["low"]["last24"] = dataList[9]

        resDict["high"]["last24"] = dataList[10]
        #en api pone que low es pos10 y high pos 9, lo hemos intercambiado

        resList.append(resDict)

    # order result by pair name
    resList = sorted(resList, key=lambda list: list["pair"])
    return JsonResponse(resList, safe=False)




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

    apidata = processRestAPIResponse(responseList)
    resList = []
    for pairData in apidata:
        resDict = getResponseDictionary()

        resDict["pair"] = normalizePairName(pairData["symbol"])
        resDict["ask"]["price"] = pairData["askPrice"]
        resDict["bid"]["price"] = pairData["bidPrice"]

        resDict["volume"]["last24"] = pairData["volume"]
        resDict["avgPrice"]["last24"] = pairData["weightedAvgPrice"]

        resDict["low"]["last24"] = pairData["lowPrice"]
        resDict["high"]["last24"] = pairData["highPrice"]
        
        resDict["opening"] = pairData["openPrice"]

        resList.append(resDict)
    # order result by pair name
    resList = sorted(resList, key=lambda list: list["pair"])
    return JsonResponse(resList, safe=False)




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

    apidata = processRestAPIResponse(responseList)

    resList = []
    for pairData in apidata:
        resDict = getResponseDictionary()

        resDict["pair"] = normalizePairName(pairData["symbol"])
        resDict["ask"]["price"] = pairData["ask"]
        resDict["bid"]["price"] = pairData["bid"]

        resDict["volume"]["last24"] = pairData["volume"]

        resDict["low"]["last24"] = pairData["low"]
        resDict["high"]["last24"] = pairData["high"]
        
        resDict["opening"] = pairData["open"]

        resList.append(resDict)

    # order result by pair name
    resList = sorted(resList, key=lambda list: list["pair"])
    return JsonResponse(resList, safe=False)





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

    apidata = processRestAPIResponse(responseList)

    resList = []
    for pairData in apidata:
        resDict = getResponseDictionary()

        resDict["pair"] = normalizePairName(pairData["instrument_id"])
        resDict["ask"]["price"] = pairData["ask"]
        resDict["bid"]["price"] = pairData["bid"]

        resDict["volume"]["last24"] = pairData["base_volume_24h"]

        resDict["low"]["last24"] = pairData["low_24h"]
        resDict["high"]["last24"] = pairData["high_24h"]
        
        resDict["opening"] = pairData["open_24h"]

        resList.append(resDict)

    # order result by pair name
    resList = sorted(resList, key=lambda list: list["pair"])
    return JsonResponse(resList, safe=False)






"""def blockchainTicker(request):
    blockchain = get_object_or_404(Exchange, name="blockchain")
    
    options = {}
    options['origin'] = 'https://exchange.blockchain.com'
    url = blockchain.api_endpoint

    blockchainCalls = []
    blockchainCalls.append('{"action": "subscribe", "channel": "prices", "symbol": "LTC-USD", "granularity": 60}')
    blockchainCalls.append('{"action": "subscribe", "channel": "prices", "symbol": "BTC-USD"}')
    blockchainCalls.append('{"action": "subscribe", "channel": "prices", "symbol": "ETH-USD"}')
    blockchainCalls.append('{"action": "subscribe", "channel": "prices", "symbol": "ETH-BTC"}')
    blockchainCalls.append('{"action": "subscribe", "channel": "prices", "symbol": "LTC-BTC"}')

    ws = create_connection(url, **options)
    
    responseList = []
    for call in blockchainCalls:
        method = "send"
        msg = call
        send =  processWebsocketAPIResponse(ws, method, msg)
        
        if send["event"] == "subscribed":
            method = "receive"
            receive =  processWebsocketAPIResponse(ws, method)

            if receive["event"] == "updated":
                responseList.append(receive)
    
    

    ws.close()
    return JsonResponse(responseList, safe=False)"""

    
