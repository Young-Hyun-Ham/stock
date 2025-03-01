import logging

def grid_strategy(trader, ticker="KRW-BTC", grid_spacing=0.02, grid_levels=5):
    """
        그리드(Grid Trading) 전략
        ▶ 개념
            지정된 가격 간격마다 자동으로 매수·매도 주문을 배치하는 방식이야.

        ▶ 전략 적용
            100만원을 10개의 구간(각 10만원)으로 나눠, 가격이 일정 구간 내에서 움직일 때마다 매수·매도 반복
            예를 들어 10% 간격으로 주문하면 가격이 10% 하락할 때마다 매수, 10% 상승할 때마다 매도
        ▶ 장점
            횡보장에서 꾸준한 수익 창출 가능
            자동화하기 용이함
        ▶ 단점
            강한 상승장이나 하락장에서는 비효율적
            수수료 부담이 커질 수 있음
    """
    try:
        base_price = trader.get_current_price(ticker)
        for i in range(1, grid_levels + 1):
            buy_condition = trader.limit_buy(ticker, base_price * (1 - grid_spacing * i), 0.001)
            sell_condition = trader.limit_sell(ticker, base_price * (1 + grid_spacing * i), 0.001)

        # logger
        if buy_condition:
            trader.logger.info(f"그리드 전략 매수 조건 충족: 가격 {base_price}")
            
        if sell_condition:
            trader.logger.info(f"그리드 전략 매도 조건 충족: 가격 {base_price}")
        
    except Exception as e:
        logging.error(f"그리드 전략 오류: {e}")