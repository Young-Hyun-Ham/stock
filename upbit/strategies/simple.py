
def simple_strategy(trader):
    try:
        trader.logger.debug("simple 전략 실행 시작")

        btc_price = trader.get_current_price("KRW-BTC")
        
        # 예시: 5% 하락시 매수, 5% 상승시 매도
        target_buy = btc_price * 0.95
        target_sell = btc_price * 1.05
        
        # 보유 현금 조회 (실제 구현 필요)
        current_krw = 100000  # 예시 금액
        
        if current_krw > 5000:
            print(f"매수 시도: {target_buy}원")
            buy_condition = trader.limit_buy("KRW-BTC", target_buy, 0.001)
        
        # 보유 코인 조회 (실제 구현 필요)
        current_btc = 0.001
        
        if current_btc > 0:
            print(f"매도 시도: {target_sell}원")
            sell_condition = trader.limit_sell("KRW-BTC", target_sell, 0.001)
        
        # logger
        if buy_condition:
            trader.logger.info(f"매수 조건 충족: 가격 {target_sell}")
            
        if sell_condition:
            trader.logger.warning(f"매도 조건 충족: 가격 {target_sell}")

    except Exception as e:
        trader.logger.critical(f"simple 전략 실행 중 치명적 오류: {str(e)}", exc_info=True)
        raise