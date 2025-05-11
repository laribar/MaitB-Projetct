from main import get_stock_data
import pandas as pd
import pytz
from datetime import datetime, timedelta

BR_TZ = pytz.timezone("America/Sao_Paulo")
start = datetime(2023, 12, 1, 10, 6, tzinfo=BR_TZ)
end = start + timedelta(hours=5)

df_candles = get_stock_data("BTC-USD", interval="1h", period="90d")
df_candles.index = pd.to_datetime(df_candles.index)
df_candles.index = df_candles.index.tz_convert(BR_TZ)

df_check = df_candles[(df_candles.index >= start) & (df_candles.index <= end)]
print("\n🧪 Candles encontrados no intervalo desejado:")
print(df_check)
