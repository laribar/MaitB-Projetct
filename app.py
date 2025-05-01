from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # 🔐 Troque por algo mais seguro em produção

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

# === Rota do dashboard ===
@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Caminho para o log e gráfico
    caminho_csv = 'prediction_log.csv'
    caminho_grafico = os.path.join('static', 'images', 'evolucao_carteira_virtual.png')

    df = pd.DataFrame()
    timeframes = []
    timeframe_selecionado = None
    sinais = []

    # 🔎 Tenta ler o CSV se existir
    if os.path.exists(caminho_csv) and os.path.getsize(caminho_csv) > 0:
        try:
            df = pd.read_csv(caminho_csv)
            if 'Timeframe' in df.columns:
                timeframes = df['Timeframe'].dropna().unique().tolist()
                timeframe_selecionado = request.args.get('timeframe', timeframes[0] if timeframes else None)
                if timeframe_selecionado:
                    sinais = df[df['Timeframe'] == timeframe_selecionado].to_dict(orient='records')
        except Exception as e:
            print(f"Erro ao ler o CSV: {e}")

    return render_template('dashboard.html',
                           usuario=session['usuario'],
                           timeframes=timeframes,
                           timeframe_selecionado=timeframe_selecionado,
                           sinais=sinais,
                           caminho_grafico=caminho_grafico)

# === Rota de logout ===
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

# === Executar o servidor Flask ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
