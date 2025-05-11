# binance_client.py
from dotenv import load_dotenv
import os
from binance.client import Client

# Carrega as variáveis do .env
load_dotenv()

# Lê as chaves da Binance Testnet
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Cria cliente apontando para a Testnet
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'
