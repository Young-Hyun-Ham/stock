import pyupbit
import logging

def bollinger_strategy(trader, ticker="KRW-BTC"):
    """
        볼린저 밴드(Bollinger Bands) 전략
        ▶ 개념
            볼린저 밴드는 이동평균선을 중심으로 상단 밴드(+2σ), 하단 밴드(-2σ)를 설정하여 가격 변동성을 측정하는 지표야.

        ▶ 전략 적용
            가격이 하단 밴드(-2σ)에 닿으면 매수
            가격이 상단 밴드(+2σ)에 닿으면 매도
            가격이 밴드 바깥으로 벗어난 후 다시 안으로 들어올 때 진입
        ▶ 장점
            변동성이 높은 시장에서 적절한 진입 타이밍을 제공
            돌파 전략(상단 밴드 돌파 시 추가 상승)과 역추세 전략(반등 기대 매수) 모두 활용 가능
        ▶ 단점
            강한 추세에서는 신호가 실패할 수 있음
            횡보장에서는 잦은 신호 발생
    """
    try:
        df = pyupbit.get_ohlcv(ticker, interval="minute15", count=20)
        mid_band = df['close'].rolling(20).mean()
        std_dev = df['close'].rolling(20).std()
        upper_band = mid_band + (std_dev * 2)
        lower_band = mid_band - (std_dev * 2)
        
        current_price = trader.get_current_price(ticker)
        if current_price < lower_band.iloc[-1]:
            buy_condition = trader.limit_buy(ticker, current_price, 0.001)
        elif current_price > upper_band.iloc[-1]:
            sell_condition = trader.limit_sell(ticker, current_price, 0.001)
        else:
            logging.info(f"볼린저 전략 조건에 맞지 않음!!")

        # logger
        if buy_condition:
            trader.logger.info(f"볼린저 전략 매수 조건 충족: 가격 {current_price}")
            
        if sell_condition:
            trader.logger.info(f"볼린저 전략 매도 조건 충족: 가격 {current_price}")

    except Exception as e:
        logging.error(f"볼린저 밴드 전략 오류: {e}")