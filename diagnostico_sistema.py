import os
import pandas as pd
import joblib
from datetime import datetime, timedelta
import pytz
import glob
import requests

BR_TZ = pytz.timezone("America/Sao_Paulo")

def verificar_flask_ativo(url="http://http://18.117.91.17:5000/"):
    print("\n🌐 Verificando status do servidor Flask...")
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ Flask ativo e respondendo em {url}")
        else:
            print(f"⚠️ Flask respondeu com status {response.status_code} — pode não estar funcionando corretamente.")
    except requests.ConnectionError:
        print(f"❌ Flask não está acessível em {url} (conexão recusada).")
    except Exception as e:
        print(f"⚠️ Erro ao verificar o Flask: {e}")

def check_log_file():
    print("📂 Verificando log.txt...")
    if os.path.exists("log.txt") and os.path.getsize("log.txt") > 0:
        print("✅ log.txt encontrado e com conteúdo.")
    else:
        print("⚠️ log.txt ausente ou vazio.")

def check_models():
    print("\n📦 Verificando modelos salvos em ./models...")
    modelos = glob.glob("models/*.h5") + glob.glob("models/*.joblib")
    if modelos:
        print(f"✅ Modelos encontrados: {len(modelos)}")
    else:
        print("⚠️ Nenhum modelo salvo encontrado.")

def check_prediction_log():
    path = "prediction_log.csv"
    print("\n📄 Verificando prediction_log.csv...")
    if not os.path.exists(path):
        print("❌ Arquivo prediction_log.csv não encontrado.")
        return None
    df = pd.read_csv(path)
    if df.empty or "Date" not in df.columns:
        print("❌ Arquivo está vazio ou mal formatado.")
        return None
    print(f"✅ prediction_log.csv com {len(df)} linhas.")
    return df

def check_ultimos_sinais(df):
    print("\n📊 Últimos sinais registrados:")
    df["Date"] = pd.to_datetime(df["Date"], utc=True).dt.tz_convert(BR_TZ)
    ultimos = df.sort_values("Date", ascending=False).head(5)
    for _, row in ultimos.iterrows():
        dt = row["Date"].strftime("%d/%m %H:%M")
        print(f"• {row['Asset']} | {row['Timeframe']} | {dt} | Sinal: {row['Signal']}")

def check_capital(df):
    if "Capital Atual" in df.columns:
        capital_final = df["Capital Atual"].dropna().values[-1]
        print(f"\n💰 Capital Atual (simulação): ${capital_final:,.2f}")
    else:
        print("⚠️ Coluna 'Capital Atual' ausente no log.")

def check_graficos():
    print("\n🖼️ Verificando gráficos salvos...")
    graficos = glob.glob("*.png") + glob.glob("static/images/*.png")
    if graficos:
        print(f"✅ {len(graficos)} gráfico(s) encontrados.")
    else:
        print("⚠️ Nenhum gráfico encontrado.")

def check_dados_candles():
    from main import get_stock_data
    print("\n📈 Verificando dados de candles...")
    df = get_stock_data("BTC-USD", interval="1h", period="30d")
    if df is not None and not df.empty and "Close" in df.columns:
        print(f"✅ Candles BTC-USD (1h): {len(df)} registros.")
    else:
        print("❌ Erro ao obter dados de candles.")

# 🚀 Executar todas as verificações
if __name__ == "__main__":
    print("🧪 Diagnóstico do Sistema de Trading (LSTM + XGBoost)\n" + "=" * 55)
    check_log_file()
    check_models()
    df_log = check_prediction_log()
    if df_log is not None:
        check_ultimos_sinais(df_log)
        check_capital(df_log)
    check_graficos()
    check_dados_candles()
    verificar_flask_ativo("http://18.117.91.17:5000")  # ou seu IP/porta real
