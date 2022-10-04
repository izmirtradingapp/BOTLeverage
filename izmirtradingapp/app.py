from flask import Flask, request
import json
from binance.client import Client
import math 


app = Flask(__name__)


@app.route("/webhook", methods=['POST'])
def webhook():

    def LongPosition(client,lev):
        assets = client.futures_account_balance()
        for asset in assets:
          if "USDT" in asset.values():
            balance = float(asset["balance"])

        markPrice = float(client.futures_mark_price(symbol="BTCUSDT")["markPrice"])
        quot = math.floor((balance/markPrice)*(95/100)*1000*lev)/1000

        params = {"symbol":"BTCUSDT",
                "type":"MARKET",
                "side":"BUY",
                "quantity":quot}
        
        try:
            ExitShortPosition(client)
            LongPos = client.futures_create_order(**params)
        except:
            LongPos = client.futures_create_order(**params)
            
    def ExitLongPosition(client):
        qty = float(client.futures_position_information(symbol="BTCUSDT")[0]["positionAmt"])
        params = {
            "symbol":"BTCUSDT",
            "side":"SELL",
            "type":'MARKET',
            "quantity":qty,
            "reduceOnly":"true"
            }
        ExitLong = client.futures_create_order(**params)


    def ShortPosition(client,lev):
        assets = client.futures_account_balance()
        for asset in assets:
          if "USDT" in asset.values():
            balance = float(asset["balance"])

        markPrice = float(client.futures_mark_price(symbol="BTCUSDT")["markPrice"])
        quot = math.floor((balance/markPrice)*(95/100)*1000*lev)/1000

        params = {"symbol":"BTCUSDT",
                "type":"MARKET",
                "side":"SELL",
                "quantity":quot}
        
        try:
            ExitLongPosition(client)
            ShortPos = client.futures_create_order(**params)
        except:
            ShortPos = client.futures_create_order(**params)

    def ExitShortPosition(client):
        qty = -(float(client.futures_position_information(symbol="BTCUSDT")[0]["positionAmt"]))
        params = {
            "symbol":"BTCUSDT",
            "side":"BUY",
            "type":'MARKET',
            "quantity":qty,
            "reduceOnly":"true"
            }
        ExitShort = client.futures_create_order(**params)

    try:
        data = json.loads(request.data)
        order = data["order"]
        lev = data["leverage"]
        api_key = data["api_key"]
        api_secret = data["api_secret"]
        
        client = Client(api_key, api_secret, testnet=False)
        client.futures_change_leverage(**{"symbol":"BTCUSDT","leverage":lev})

        if order == "LongPosition":
            LongPosition(client,lev)

        elif order == "ExitLongPosition":
            ExitLongPosition(client)
          
        elif order == "ShortPosition":
            ShortPosition(client,lev)

        elif order == "ExitShortPosition":
            ExitShortPosition(client)

    except Exception as e:
        print(e)
        pass
    return {
        "code": "success",

    }
