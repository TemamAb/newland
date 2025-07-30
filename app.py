from flask import Flask, jsonify
from core.dashboard import monitor

app = Flask(__name__)

@app.route('/metrics')
def get_metrics():
    return jsonify({
        "deployed": monitor.deployed,
        "active": monitor.active,
        "capacity": monitor.maxCapacity
    })

@app.route('/update/<int:deployed>/<int:active>')
def update_metrics(deployed, active):
    monitor.updateCounts(deployed, active)
    return jsonify({"status": "updated"})
@app.route('/wallet/connect')
def wallet_connect():
    return jsonify({
        "bridge": "https://bridge.walletconnect.org",
        "methods": ["eth_sendTransaction", "personal_sign"]
    })
