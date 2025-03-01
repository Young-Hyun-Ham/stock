from strategies.simple import simple_strategy
from strategies.moving_average import moving_average_strategy
from strategies.rsi import rsi_strategy
from strategies.bollinger import bollinger_strategy
from strategies.trend_following import trend_following_strategy
from strategies.martingale import martingale_strategy
from strategies.grid import grid_strategy
from strategies.macd import macd_strategy

def trading_strategy(trader, strategy_type):
    """ 전략 관리 """
    strategies = {
        "simple": simple_strategy,
        "moving_average": moving_average_strategy,
        "rsi": rsi_strategy,
        "bollinger": bollinger_strategy,
        "trend_following": trend_following_strategy,
        "martingale": martingale_strategy,
        "grid": grid_strategy,
        "macd": macd_strategy,
    }
    
    strategy_func = strategies.get(strategy_type)
    if strategy_func:
        strategy_func(trader)
    else:
        trader.logger.warning(f"지원되지 않는 전략: {strategy_type}")
