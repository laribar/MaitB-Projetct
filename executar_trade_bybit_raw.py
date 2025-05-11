# executar_trade_bybit_raw.py
import requests
import time
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")
BASE_URL = "https://api-testnet.bybit.com"  # Testnet

def gerar_assinatura(params, secret):
    ordered = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    return hmac.new(
        bytes(secret, "utf-8"),
        msg=bytes(ordered, "utf-8"),
        digestmod=hashlib.sha256
    ).hexdigest()

def executar_ordem_market(symbol="BTCUSDT", side="Buy", valor_usdt=10):
    # Passo 1: Obter preço atual
    preco_resp = requests.get(f"{BASE_URL}/v5/market/tickers", params={
        "category": "spot",
        "symbol": symbol
    })
    preco_data = preco_resp.json()
    preco_atual = float(preco_data["result"]["list"][0]["lastPrice"])
    quantidade = round(valor_usdt / preco_atual, 6)

    print(f"📈 Preço atual: {preco_atual}")
    print(f"🟢 Enviando ordem {side} de {quantidade} {symbol}")

    # Passo 2: Montar os parâmetros da ordem
    timestamp = int(time.time() * 1000)
    params = {
        "apiKey": API_KEY,
        "symbol": symbol,
        "side": side,
        "orderType": "Market",
        "qty": str(quantidade),
        "category": "spot",
        "timestamp": timestamp,
        "recvWindow": 5000
    }
    sign = gerar_assinatura(params, API_SECRET)
    params["sign"] = sign

    # Passo 3: Enviar ordem
    response = requests.post(f"{BASE_URL}/v5/order/create", params=params)
    resultado = response.json()
    print("📦 Resultado da ordem:")
    print(resultado)

if __name__ == "__main__":
    executar_ordem_market()
