# bybit_client.py
import os
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

# Carrega variáveis do arquivo .env
load_dotenv()

# Lê as chaves da Bybit Testnet
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")

# Cria sessão com a Bybit Testnet (modo Unified V5)
session = HTTP(
    testnet=True,
    api_key=API_KEY,
    api_secret=API_SECRET
)
