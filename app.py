from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Rota de login
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

# Rota do dashboard
@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Carregar dados
    df = pd.read_csv('prediction_log.csv')
    timeframes = df['timeframe'].unique()
    timeframe_selecionado = request.args.get('timeframe', timeframes[0])
    df_filtrado = df[df['timeframe'] == timeframe_selecionado]

    # Caminho para o gráfico
    caminho_grafico = os.path.join('static', 'images', 'evolucao_carteira_virtual.png')

    return render_template('dashboard.html',
                           usuario=session['usuario'],
                           timeframes=timeframes,
                           timeframe_selecionado=timeframe_selecionado,
                           sinais=df_filtrado.to_dict(orient='records'),
                           caminho_grafico=caminho_grafico)

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

# ... (suas rotas e outras funções acima)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

