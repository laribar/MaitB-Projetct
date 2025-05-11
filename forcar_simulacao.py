from main import simular_todos_trades, get_stock_data, calculate_indicators

# Baixar candles históricos
df_candles = get_stock_data("BTC-USD", interval="1h", period="90d")
df_candles = calculate_indicators(df_candles)

# Rodar a simulação forçada
simular_todos_trades(
    prediction_log_path="prediction_log.csv",
    df_candles=df_candles,
    timeframe="1h"
)
