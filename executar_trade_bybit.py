# executar_trade_bybit.py
from bybit_client import session

def executar_ordem_spot_bybit(symbol="BTCUSDT", valor_usdt=10):
    try:
        # ✅ Corrigido: busca preço atual
        book = session.get_market_tickers(category="spot", symbol=symbol)
        preco = float(book["result"]["list"][0]["lastPrice"])
        quantidade = round(valor_usdt / preco, 6)

        print(f"📈 Preço atual de {symbol}: {preco}")
        print(f"🟢 Enviando ordem de COMPRA no Spot: {quantidade} {symbol} (≈ {valor_usdt} USDT)")

        order = session.place_order(
            category="spot",
            symbol=symbol,
            side="Buy",
            order_type="Market",
            qty=str(quantidade)
        )

        print("✅ Ordem executada com sucesso!")
        print(order)

    except Exception as e:
        print(f"❌ Erro ao executar ordem: {e}")

if __name__ == "__main__":
    executar_ordem_spot_bybit()
