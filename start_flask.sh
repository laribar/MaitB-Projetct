#!/bin/bash
source venv/bin/activate
nohup python app.py --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
echo "✅ Flask iniciado em background. Logs em flask.log"
