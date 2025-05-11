import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

BR_TZ = pytz.timezone("America/Sao_Paulo")

# Gera candles simulados a partir de 2023-12-01 10:00:00
inicio = datetime(2023, 12, 1, 10, 0, tzinfo=BR_TZ)
datas = [inicio + timedelta(hours=i) for i in range(6)]

df_candles = pd.DataFrame({
    "Open": [29500, 29700, 29900, 30100, 30300, 30500],
    "High": [29600, 29800, 30000, 30200, 30400, 30600],
    "Low":  [29400, 29600, 29800, 30000, 30200, 30400],
    "Close": [29550, 29750, 29950, 30150, 30350, 30550],
    "Volume": [10, 12, 11, 14, 13, 15]
}, index=pd.DatetimeIndex(datas, name="Date"))

# Salva em pickle
df_candles.to_pickle("df_candles_teste.pkl")
print("✅ df_candles_teste.pkl salvo com sucesso.")
