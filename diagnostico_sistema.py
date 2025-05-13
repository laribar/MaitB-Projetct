import os
import pandas as pd
from datetime import datetime
from pytz import timezone
import subprocess

# Configurações
BR_TZ = timezone("America/Sao_Paulo")
LOG_PATH = "./log.txt"
CSV_PATH = "./prediction_log.csv"
MODELS_DIR = "./models"
STATIC_IMG_DIR = "./static/images"
GRAFICOS_CHAVE = ["candle_proj_", "previsao_vs_real", "evolucao_carteira"]

# Funções de diagnóstico
def print_header():
    print("🧪 Diagnóstico do Sistema de Trading (LSTM + XGBoost)")
    print("=" * 55)

def check_log_file():
    print("📂 Verificando log.txt...")
    if os.path.exists(LOG_PATH) and os.path.getsize(LOG_PATH) > 0:
        print("✅ log.txt encontrado e com conteúdo.")
    else:
        print("❌ log.txt não encontrado ou vazio.")

def check_models():
    print("\n📦 Verificando modelos salvos em ./models...")
    if not os.path.exists(MODELS_DIR):
        print("❌ Pasta de modelos não encontrada.")
        return
    modelos = [f for f in os.listdir(MODELS_DIR) if f.endswith((".joblib", ".h5"))]
    if modelos:
        print(f"✅ Modelos encontrados: {len(modelos)}")
    else:
        print("⚠️ Nenhum modelo encontrado.")

def check_prediction_log():
    print("\n📄 Verificando prediction_log.csv...")
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        print("❌ prediction_log.csv não encontrado ou está vazio.")
        return None
    try:
        df = pd.read_csv(CSV_PATH)
        print(f"✅ prediction_log.csv com {len(df)} linhas.")
        return df
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return None

def check_ultimos_sinais(df):
    print("\n📊 Últimos sinais registrados:")
    try:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date", ascending=False).head(5)
        for _, row in df.iterrows():
            data = row["Date"].strftime("%d/%m %H:%M")
            asset = row.get("Asset", "N/A")
            tf = row.get("Timeframe", "N/A")
            signal = row.get("Signal", "N/A")
            print(f"• {asset} | {tf} | {data} | Sinal: {signal}")
    except Exception as e:
        print(f"⚠️ Erro ao analisar últimos sinais: {e}")



print("\n🧠 Verificando processos Python ativos (main.py, app.py)...")
try:
    result = subprocess.check_output(["ps", "aux"])
    lines = result.decode("utf-8").splitlines()
    python_lines = [line for line in lines if "python" in line and ("main.py" in line or "app.py" in line)]

    if not python_lines:
        print("⚠️ Nenhum processo Python relacionado a main.py ou app.py está rodando.")
    else:
        for line in python_lines:
            print(f"✅ {line}")
except Exception as e:
    print(f"❌ Erro ao verificar processos: {e}")

def check_capital(df):
    print("\n💰 Verificando Capital da Carteira Virtual...")
    if "Capital Atual" not in df.columns:
        print("⚠️ Coluna 'Capital Atual' não existe no log.")
        return
    df["Capital Atual"] = pd.to_numeric(df["Capital Atual"], errors="coerce")
    capital_vals = df["Capital Atual"].dropna()
    if capital_vals.empty:
        print("⚠️ Nenhum valor disponível na coluna 'Capital Atual'.")
        return
    capital_inicial = capital_vals.iloc[0]
    capital_final = capital_vals.iloc[-1]
    roi = ((capital_final / capital_inicial) - 1) * 100 if capital_inicial != 0 else 0
    print(f"• Capital Inicial: ${capital_inicial:,.2f}")
    print(f"• Capital Final  : ${capital_final:,.2f}")
    print(f"• ROI Total      : {roi:+.2f}%")

def check_flask_server():
    print("\n🌐 Verificando status do servidor Flask...")
    try:
        result = subprocess.check_output(["pgrep", "-f", "app.py"]).decode().strip()
        if result:
            print("✅ Flask em execução (PID(s):", result + ")")
        else:
            print("❌ Flask não está rodando.")
    except subprocess.CalledProcessError:
        print("❌ Flask não está rodando.")

def check_graficos_static():
    print("\n🖼️ Verificando presença dos gráficos no dashboard...")
    if not os.path.exists(STATIC_IMG_DIR):
        print("❌ Pasta de imagens não encontrada.")
        return
    arquivos = os.listdir(STATIC_IMG_DIR)
    encontrados = [f for f in arquivos if any(chave in f for chave in GRAFICOS_CHAVE)]
    if encontrados:
        print(f"✅ Gráficos encontrados: {len(encontrados)}")
        for f in encontrados:
            print(f"  • {f}")
    else:
        print("⚠️ Nenhum gráfico encontrado no diretório static/images.")

# Execução principal
if __name__ == "__main__":
    print_header()
    check_log_file()
    check_models()
    df_log = check_prediction_log()
    if df_log is not None:
        check_ultimos_sinais(df_log)
        check_capital(df_log)
    check_flask_server()
    check_graficos_static()
