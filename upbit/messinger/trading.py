import asyncio
from collections import defaultdict
import json
import os
import time
from dotenv import load_dotenv
import requests
import pandas as pd
import requests
import websockets

from datetime import datetime, timedelta, timezone

# config 폴더 안에 있는 .env 파일 경로
dotenv_path = os.path.join('config', '.env')

# 환경 변수 로드
load_dotenv(dotenv_path)

# 업비트 WebSocket 주소
UPBIT_WS_URL = "wss://api.upbit.com/websocket/v1"

# 업비트 REST API를 이용해 KRW 마켓 종목 가져오기
UPBIT_MARKET_URL = "https://api.upbit.com/v1/market/all"

# 텔레그램 봇 설정
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # 👉 BotFather에서 받은 API Token 입력
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # 👉 대화방 ID 입력 (그룹이면 -123456 형식)

# 업비트 REST API를 이용해 KRW 마켓 종목 가져오기
async def fetch_krw_markets():
    response = requests.get(UPBIT_MARKET_URL)
    if response.status_code != 200:
        print(f"⚠️ 업비트 마켓 정보를 가져오지 못했습니다. 상태 코드: {response.status_code}")
        return []

    market_data = response.json()
    return [m['market'] for m in market_data if m['market'].startswith('KRW-')]


async def get_top_10_trading_volume():
    # 모든 KRW 마켓 구독 요청 생성
    krw_markets = await fetch_krw_markets()
    subscribe = [{"ticket": "realtime"}, {"type": "ticker", "codes": krw_markets}]

    async with websockets.connect(UPBIT_WS_URL) as websocket:
        await websocket.send(json.dumps(subscribe))
        
        trading_volumes = defaultdict(float)  # 거래량을 저장할 딕셔너리
        start_time = asyncio.get_event_loop().time()  # 10분 측정용 시작 시간

        while True:
            data = await websocket.recv()
            json_data = json.loads(data)

            market = json_data["code"]
            volume = json_data["acc_trade_volume"]  # 현재 24시간 누적 거래량

            trading_volumes[market] = volume  # 거래량 업데이트

            # 10초이 지나면 종료 후 상위 10개 종목 출력
            if asyncio.get_event_loop().time() - start_time > 10:
                break

        # 거래량 기준 상위 10개 종목 정렬
        top_10 = sorted(trading_volumes.items(), key=lambda x: x[1], reverse=True)[:10]

        print("\n📊 최근 10분간 거래량 TOP 10 종목:")
        for rank, (market, volume) in enumerate(top_10, start=1):
            print(f"{rank} => 종목: {market}, 거래량: {volume:.2f}")
        
        # 📩 Telegram 메시지 전송
        message = "\n📊 최근 10분간 거래량 TOP 10 종목:\n"
        for rank, (market, volume) in enumerate(top_10, start=1):
            message += f"{rank}. {market}: {volume:.2f}\n"

        send_telegram_message(message)

def send_telegram_message(message):
    """ Telegram 메시지 전송 함수 """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("✅ 텔레그램 메시지 전송 완료!")
    else:
        print(f"⚠️ 텔레그램 메시지 전송 실패! 상태 코드: {response.status_code}")

# 실행 및 결과 출력
if __name__ == "__main__":
    asyncio.run(get_top_10_trading_volume())
