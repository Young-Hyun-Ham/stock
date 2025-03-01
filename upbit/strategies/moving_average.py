import pyupbit
import logging

def moving_average_strategy(trader, ticker="KRW-BTC"):
    """
        이동평균선(Moving Average) 전략
        ▶ 개념
            이동평균선(MA)은 일정 기간 동안의 가격 평균을 나타내는 지표야.
            단기 MA와 장기 MA를 비교하여 매수/매도 타이밍을 잡을 수 있다.

        ▶ 전략 적용
            단기(5일) MA가 장기(20일) MA를 상향 돌파하면 매수 (골든크로스)
            단기 MA가 장기 MA를 하향 돌파하면 매도 (데드크로스)
        ▶ 장점
            비교적 단순하고 신뢰성이 높음
            중장기 트레이딩에 적합
        ▶ 단점
            변동성이 큰 시장에서는 신호가 늦을 수 있음
            횡보장에서는 잦은 매매로 수익성이 낮아질 수 있음
    """
    try:
        short_ma = pyupbit.get_ohlcv(ticker, interval="minute15", count=10)['close'].mean()
        long_ma = pyupbit.get_ohlcv(ticker, interval="minute15", count=50)['close'].mean()
        
        if short_ma > long_ma:
            buy_condition = trader.limit_buy(ticker, trader.get_current_price(ticker), 0.001)
        elif short_ma < long_ma:
            sell_condition = trader.limit_sell(ticker, trader.get_current_price(ticker), 0.001)
        else:
            trader.trade_log(ticker, trader.get_current_price(ticker), 0.001)
            logging.info(f"이동평균선 전략 조건에 맞지 않음!!")

        # logger
        if buy_condition:
            trader.logger.info(f"이동평균선 전략 매수 조건 충족: 가격 {current_price}")
            
        if sell_condition:
            trader.logger.info(f"이동평균선 전략 매도 조건 충족: 가격 {current_price}")
    except Exception as e:
        logging.error(f"이동평균선 전략 오류: {e}")