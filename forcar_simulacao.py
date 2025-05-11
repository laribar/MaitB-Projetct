from simular_trade import simular_todos_trades
from get_stock_data import get_stock_data
from calculate_indicators import calculate_indicators

df_candles = get_stock_data("BTC-USD", interval="1h", period="90d")
df_candles = calculate_indicators(df_candles)

simular_todos_trades(
    prediction_log_path="prediction_log.csv",
    df_candles=df_candles,
    timeframe="1h"
)
