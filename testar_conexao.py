# testar_conexao.py
from binance_client import client

def testar_conexao():
    try:
        info = client.get_account()
        print("✅ Conexão bem-sucedida com Binance Testnet!")
        print(f"Saldo disponível:")
        for saldo in info["balances"]:
            if float(saldo["free"]) > 0:
                print(f"• {saldo['asset']}: {saldo['free']}")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")

if __name__ == "__main__":
    testar_conexao()
