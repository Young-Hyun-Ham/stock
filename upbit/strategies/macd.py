import pyupbit
import logging

def macd_strategy(trader, ticker="KRW-BTC"):
    """
        MACD (이동평균 수렴·확산지수) 전략
        ▶ 개념
            MACD는 두 개의 이동평균선(빠른 EMA, 느린 EMA) 간의 차이를 나타내는 지표야.

        ▶ 전략 적용
            MACD가 시그널선 위로 교차하면 매수 신호 (골든크로스)
            MACD가 시그널선 아래로 교차하면 매도 신호 (데드크로스)
        ▶ 장점
            트렌드를 잘 따라가는 전략
            노이즈가 적어 신뢰성이 높음
        ▶ 단점
            신호가 느릴 수 있음
            변동성이 큰 시장에서는 다소 부정확할 수 있음
    """
    try:
        df = pyupbit.get_ohlcv(ticker, interval="minute15", count=50)
        short_ema = df['close'].ewm(span=12, adjust=False).mean()
        long_ema = df['close'].ewm(span=26, adjust=False).mean()
        macd = short_ema - long_ema
        signal = macd.ewm(span=9, adjust=False).mean()
        
        if macd.iloc[-1] > signal.iloc[-1]:
            buy_condition = trader.limit_buy(ticker, trader.get_current_price(ticker), 0.001)
        elif macd.iloc[-1] < signal.iloc[-1]:
            sell_condition = trader.limit_sell(ticker, trader.get_current_price(ticker), 0.001)
        else:
            logging.info(f"MACD (이동평균 수렴·확산지수) 전략 조건에 맞지 않음!!")
            
        # logger
        if buy_condition:
            trader.logger.info(f"MACD (이동평균 수렴·확산지수) 전략 매수 조건 충족: 가격 {trader.get_current_price(ticker)}")
            
        if sell_condition:
            trader.logger.info(f"MACD (이동평균 수렴·확산지수) 전략 매도 조건 충족: 가격 {trader.get_current_price(ticker)}")

    except Exception as e:
        logging.error(f"MACD (이동평균 수렴·확산지수) 전략 오류: {e}")