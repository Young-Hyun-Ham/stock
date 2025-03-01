import logging

def martingale_strategy(trader, ticker="KRW-BTC", base_volume=0.001, max_attempts=5):
    """
        마틴게일(Martingale) 전략
        ▶ 개념
            손실이 날 때마다 배팅 금액을 2배씩 늘려서 이전 손실을 만회하는 전략이야.

        ▶ 전략 적용
            처음 10만원 매수 후 하락 시 20만원 추가 매수
            다시 하락하면 40만원 추가 매수 … 반복
            반등하면 총 매입금액 대비 수익 발생 후 전량 매도
        ▶ 장점
            높은 확률로 손실 회복 가능
            평균 매입 단가를 낮출 수 있음
        ▶ 단점
            큰 하락장이 오면 감당할 수 없는 손실 발생
            자본력이 충분해야 함
     """
    try:
        attempts = 0
        while attempts < max_attempts:
            current_price = trader.get_current_price(ticker)
            buy_condition = trader.limit_buy(ticker, current_price, base_volume * (2 ** attempts))
            # logger
            if buy_condition:
                trader.logger.info(f"마틴게일 전략 매수 조건 충족: 가격 {current_price}")
                
            attempts += 1
        

    except Exception as e:
        logging.error(f"마틴게일 전략 오류: {e}")