import json
import requests
import websockets
import asyncio

async def realtime_price():
    uri = "wss://api.upbit.com/websocket/v1"
    subscribe = [{"ticket":"realtime"}, {"type":"ticker", "codes":["KRW-BTC"]}]
    
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(subscribe))
        while True:
            data = await websocket.recv()
            json_data = json.loads(data)
            print(f"[실시간] {json_data['trade_price']}원")

def get_balance(self, currency="KRW"):
    url = self.server_url + "/accounts"
    headers = self._get_headers()
    res = requests.get(url, headers=headers)
    for asset in res.json():
        if asset['currency'] == currency:
            return float(asset['balance'])
    return 0