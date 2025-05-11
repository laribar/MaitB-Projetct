# forcar_simulacao.py
import pandas as pd
from main import get_stock_data, calculate_indicators, simular_todos_trades

from datetime import datetime
import pytz

# Configuração do fuso horário
BR_TZ = pytz.timezone("America/Sao_Paulo")

# === Parâmetros do ativo e timeframe ===
asset = "BTC-USD"
interval = "1h"
period = "90d"

# === Coleta dos dados ===
print(f"⏳ Usando period para {asset} ({interval}): {period}")
df_candles = get_stock_data(asset, interval=interval, period=period)
df_candles = calculate_indicators(df_candles)

# === Garantir timezone correto ===
df_candles.index = pd.to_datetime(df_candles.index)
if df_candles.index.tz is None:
    df_candles.index = df_candles.index.tz_localize("UTC").tz_convert(BR_TZ)
else:
    df_candles.index = df_candles.index.tz_convert(BR_TZ)

# === Verificar intervalo de candles ===
start_date = df_candles.index.min()
end_date = df_candles.index.max()
print(f"\n📆 Verificando range de df_candles: {start_date} ➔ {end_date}")

# === Rodar a simulação forçada ===
simular_todos_trades(
    prediction_log_path="prediction_log.csv",
    df_candles=df_candles,
    timeframe=interval
)
