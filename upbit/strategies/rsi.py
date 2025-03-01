import pyupbit
import logging

def get_rsi(data, period=14):
    """ RSI 계산 """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def rsi_strategy(trader, ticker="KRW-BTC"):
    """
        상대강도지수(RSI) 기반 과매수/과매도 전략
        ▶ 개념
            RSI(상대강도지수)는 0~100 사이의 값으로 시장의 과열 여부를 판단하는 지표.

        ▶ 전략 적용
            RSI > 70 → 과매수 상태 (매도 신호)
            RSI < 30 → 과매도 상태 (매수 신호)
        ▶ 장점
            시장이 과열됐을 때 빠른 대응 가능
            반등 구간에서 매수 타이밍을 잡을 수 있음
        ▶ 단점
            횡보장에서 신뢰도가 낮아질 수 있음
            강한 상승장에서는 70 이상에서도 계속 상승할 수 있음
    """
    try:
        df = pyupbit.get_ohlcv(ticker, interval="minute15", count=15)
        rsi = get_rsi(df['close']).iloc[-1]
        
        if rsi < 30:
            buy_condition = trader.limit_buy(ticker, trader.get_current_price(ticker), 0.001)
        elif rsi > 70:
            sell_condition = trader.limit_sell(ticker, trader.get_current_price(ticker), 0.001)
        else:
            logging.info(f"RSI 전략 조건에 맞지 않음!!")

        # logger
        if buy_condition:
            trader.logger.info(f"RSI 전략 매수 조건 충족: 가격 {current_price}")
            
        if sell_condition:
            trader.logger.info(f"RSI 전략 매도 조건 충족: 가격 {current_price}")
    except Exception as e:
        logging.error(f"RSI 전략 오류: {e}")