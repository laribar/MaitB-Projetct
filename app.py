from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
import shutil

from main import plotar_grafico_carteira_virtual, run_analysis  # ajuste o nome se o seu script principal for diferente

# app.py
app = Flask(__name__)

@app.route("/ping")
def ping():
    return "pong", 200

app.secret_key = 'sua_chave_secreta'  # troque por algo seguro em produção

# === Rota de login ===
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']
        if usuario == 'admin' and senha == 'senha123':
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', erro='Credenciais inválidas.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Caminhos
    caminho_csv = 'prediction_log.csv'
    caminho_imagem_destino = 'static/images/evolucao_carteira_virtual.png'
    caminho_imagem_origem = 'evolucao_carteira_virtual.png'

    # === Verificação e geração do gráfico da carteira virtual ===
    if not os.path.exists(caminho_imagem_destino):
        try:
            if os.path.exists(caminho_csv):
                plotar_grafico_carteira_virtual()
                from main import mover_graficos_para_static
                mover_graficos_para_static()

                if os.path.exists(caminho_imagem_destino):
                    print("✅ Gráfico da carteira movido para o dashboard.")
                else:
                    print("⚠️ Gráfico não foi gerado ou movido corretamente.")
            else:
                print("⚠️ Arquivo de log não encontrado. Gráfico não será gerado.")
        except Exception as e:
            print(f"❌ Erro ao gerar ou mover gráfico da carteira: {e}")

    # Carregamento do CSV
    df = pd.DataFrame()
    timeframes = []
    timeframe_selecionado = None
    sinais = []

    if os.path.exists(caminho_csv) and os.path.getsize(caminho_csv) > 0:
        try:
            df = pd.read_csv(caminho_csv)
            if 'Timeframe' in df.columns:
                timeframes = df['Timeframe'].dropna().unique().tolist()
                timeframe_selecionado = request.args.get('timeframe', timeframes[0] if timeframes else None)
                if timeframe_selecionado:
                    df_filtrado = df[(df['Timeframe'] == timeframe_selecionado) & (df['LSTM_PRED_CLOSE'].notna())]
                    sinais = df_filtrado.to_dict(orient='records')
        except Exception as e:
            print(f"Erro ao carregar o prediction_log.csv: {e}")

    mensagem = request.args.get('mensagem')




    return render_template('dashboard.html',
                           usuario=session['usuario'],
                           timeframes=timeframes,
                           timeframe_selecionado=timeframe_selecionado,
                           sinais=sinais,
                           caminho_grafico=caminho_imagem_destino,
                           mensagem=mensagem)

# === Rota de re-treinamento manual ===
@app.route('/retrain', methods=['POST'])
def retrain():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    try:
        run_analysis(retrain_models=True)
        mensagem = "✅ Re-treinamento iniciado com sucesso!"
    except Exception as e:
        mensagem = f"❌ Erro ao iniciar re-treinamento: {e}"

    return redirect(url_for('dashboard', mensagem=mensagem))

# === Rota de logout ===
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


