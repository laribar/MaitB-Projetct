from flask import Flask, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def home():
    log_path = "prediction_log.csv"
    df = pd.read_csv(log_path) if os.path.exists(log_path) else pd.DataFrame()
    df = df.sort_values("Date", ascending=False).head(20)
    return render_template("dashboard.html", signals=df.to_dict(orient="records"))

@app.route("/grafico")
def grafico():
    path = "evolucao_carteira_virtual.png"
    if os.path.exists(path):
        return send_file(path, mimetype="image/png")
    return "Gráfico não encontrado", 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
