import logging
from logging.handlers import TimedRotatingFileHandler
from trading_strategy import trading_strategy
import os
import sys
import jwt
import pyupbit
import requests
import time
import json
import hashlib
import hmac
from dotenv import load_dotenv
import websockets

# config 폴더 안에 있는 .env 파일 경로
dotenv_path = os.path.join('config', '.env')

# 환경 변수 로드
load_dotenv(dotenv_path)

class UpbitTrader:
    def __init__(self):
        self.access_key = os.getenv("UPBIT_ACCESS_KEY")
        self.secret_key = os.getenv("UPBIT_SECRET_KEY")
        self.server_url = "https://api.upbit.com/v1"
        self._init_logger() # 로거 초기화
        
    def _init_logger(self):
        """로깅 시스템 초기화"""
        self.logger = logging.getLogger("UpbitTrader")
        self.logger.setLevel(logging.DEBUG)

        # 포매터 설정
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(module)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 파일 핸들러 (일별 로그 분할)
        file_handler = TimedRotatingFileHandler(
            'trading_log.log',
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 예외 처리 핸들러
        sys.excepthook = self.handle_exception

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """전역 예외 처리"""
        self.logger.error(
            "글로벌 예외 발생!",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

    def _get_headers(self, query=None):
        payload = {
            "access_key": self.access_key,
            "nonce": str(int(time.time() * 1000)),
        }
        if query:
            payload["query"] = query
        
        jwt_token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return {"Authorization": f"Bearer {jwt_token}"}

    # 현재 가격 조회
    def get_current_price(self, ticker="KRW-BTC"):
        try:
            url = "https://api.upbit.com/v1/ticker"
            params = {"markets": ticker}
            res = requests.get(url, params=params)
            price = res.json()[0]["trade_price"]

            # logger
            self.logger.info(f"{ticker} 현재가 조회: {price}")
            return price
        except Exception as e:
            self.logger.error(f"가격 조회 실패: {str(e)}")
            raise    

    # 지정가 매수 주문
    def limit_buy(self, ticker, price, volume):
        try:
            query = {
                "market": ticker,
                "side": "bid",
                "volume": str(volume),
                "price": str(price),
                "ord_type": "limit"
            }
            headers = self._get_headers(query=json.dumps(query))
            res = requests.post(
                self.server_url + "/orders",
                json=query,
                headers=headers
            )
            
            # logger
            self.logger.info(
                f"매수 주문 성공 - {ticker} "
                f"가격: {price}, 수량: {volume}, 응답: {res.json()}"
            )
            return res.json()
        except Exception as e:
            self.logger.error(f"매수 주문 실패: {str(e)}")
            raise

    # 지정가 매도 주문
    def limit_sell(self, ticker, price, volume):
        try: 
            query = {
                "market": ticker,
                "side": "ask",
                "volume": str(volume),
                "price": str(price),
                "ord_type": "limit"
            }
            headers = self._get_headers(query=json.dumps(query))
            res = requests.post(
                self.server_url + "/orders",
                json=query,
                headers=headers
            )

            # logger
            self.logger.info(
                f"매도 주문 성공 - {ticker} "
                f"가격: {price}, 수량: {volume}, 응답: {res.json()}"
            )
            return res.json()
        except Exception as e:
            self.logger.error(f"매도 주문 실패: {str(e)}")
            raise
    
    # 트레이드 로그 함수
    def trade_log(self, ticker, price, volume):
        try:
            self.logger.info(
                f"ticker name - {ticker} "
                f"가격: {price}, 수량: {volume}"
            )
        except Exception as e:
            self.logger.error(f"테스트트 실패: {str(e)}")
            raise
    
if __name__ == "__main__":
    #print(f"access key : {os.getenv("UPBIT_ACCESS_KEY")}")
    #print(f"secret key : {os.getenv("UPBIT_SECRET_KEY")}")
    trader = UpbitTrader()
    trader.logger.info("====== 자동 매매 프로그램 시작 ======")
    isRun = True

    try:
        while isRun:
            #trading_strategy(trader, "simple")
            #trading_strategy(trader, "moving_average")
            #trading_strategy(trader, "rsi")
            #trading_strategy(trader, "bollinger")
            trading_strategy(trader, "trend_following")
            #trading_strategy(trader, "martingale")
            #trading_strategy(trader, "grid")
            #trading_strategy(trader, "macd")
            isRun = False
            #time.sleep(60)  # 1분 간격 실행

    except KeyboardInterrupt:
        trader.logger.info("사용자에 의해 프로그램 종료")
    except Exception as e:
        trader.logger.critical(f"프로그램 비정상 종료: {str(e)}", exc_info=True)
    finally:
        trader.logger.info("====== 프로그램 종료 ======")

# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
# ▼▼▼ 주요 기능 확장 ▼▼▼

# 실시간 가격 가져오기기
async def realtime_price():
    uri = "wss://api.upbit.com/websocket/v1"
    subscribe = [{"ticket":"realtime"}, {"type":"ticker", "codes":["KRW-BTC"]}]
    
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(subscribe))
        while True:
            data = await websocket.recv()
            json_data = json.loads(data)
            print(f"[실시간] {json_data['trade_price']}원")

# 사용자의 계좌 정보를 조회
def get_balance(self, currency="KRW"):
    url = self.server_url + "/accounts"
    headers = self._get_headers()
    res = requests.get(url, headers=headers)
    for asset in res.json():
        if asset['currency'] == currency:
            return float(asset['balance'])
    return 0

# 특정 종목(ticker)의 시세 데이터
def get_ma15(ticker):
    # interval="minute15" → 15분 봉 데이터 (15분마다 한 개의 캔들)
    # count=20 → 최근 20개의 15분 봉 데이터를 가져옴
    df = pyupbit.get_ohlcv(ticker, interval="minute15", count=20)
    # df['close'] → 종가(close) 열을 선택
    # .rolling(15).mean() → 15개의 15분 봉을 기준으로 이동평균(15MA) 계산
    # .iloc[-1] → 가장 최근 값 (즉, 최신 15MA 값) 반환
    return df['close'].rolling(15).mean().iloc[-1]
    
# ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒