import pyupbit
import logging

def trend_following_strategy(trader, ticker="KRW-BTC"):
    """
        추세추종(Trend Following) 전략
        ▶ 개념
            추세가 있는 시장에서 "오를 때 사고, 내릴 때 판다" 를 기본 원칙으로 하는 전략이야.

        ▶ 전략 적용
            상승 추세가 명확할 때 진입 후 보유 (ex. 이동평균선, MACD 사용)
            하락 추세가 지속되면 매도 후 대기
        ▶ 장점
            상승장이 지속될 경우 큰 수익 가능
            단기 트레이딩보다 적은 매매로 수익 극대화 가능
        ▶ 단점
            횡보장에서 수익이 나지 않을 수 있음
            추세 전환을 잘못 판단하면 손실이 커질 수 있음
    """
    try:
        df = pyupbit.get_ohlcv(ticker, interval="day", count=50)
        trend = df['close'].rolling(20).mean().iloc[-1]
        current_price = trader.get_current_price(ticker)
        
        if current_price > trend:
            buy_condition = trader.limit_buy(ticker, current_price, 0.001)
        elif current_price < trend:
            sell_condition = trader.limit_sell(ticker, current_price, 0.001)
        else:
            logging.info(f"추세추종 전략 조건에 맞지 않음!!")

        # logger
        if buy_condition:
            trader.logger.info(f"추세추종 전략 매수 조건 충족: 가격 {current_price}")
            
        if sell_condition:
            trader.logger.info(f"추세추종 전략 매도 조건 충족: 가격 {current_price}")
    except Exception as e:
        logging.error(f"추세추종 전략 오류: {e}")