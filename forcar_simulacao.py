import pandas as pd
from main import simular_todos_trades

# 🔧 Carrega candles simulados manualmente
df_candles = pd.read_pickle("df_candles_teste.pkl")

# ✅ Rodar simulação de carteira com os dados de teste
simular_todos_trades(
    prediction_log_path="prediction_log.csv",
    df_candles=df_candles,
    timeframe="1h"
)
