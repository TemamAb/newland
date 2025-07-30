from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Newland app is deployed and running!"
from flask import Flask, render_template_string, jsonify
import re
from collections import defaultdict
from datetime import datetime
import os

app = Flask(__name__)

LOG_PATH = os.getenv("LOG_FILE", "newland_errors.log")
CSV_PATH = os.getenv("PROFIT_CSV", f"newland_profits_{datetime.now().strftime('%Y%m%d')}.csv")

bot_profits = defaultdict(float)
bot_status = defaultdict(str)
total_profit = 0.0
mev_attacks = 0
latencies = []

P_PROFIT = re.compile(r'\[BOT:(.*?)\].*?TRADE:.*?PROFIT: ([0-9.]+)')
P_LATENCY = re.compile(r'LATENCY: ([0-9]+)ms')
P_MEV = re.compile(r'TYPE:MEV|FRONTRUN|SANDWICH')

def process_logs():
    global total_profit, mev_attacks
    if not os.path.exists(LOG_PATH): return
    with open(LOG_PATH) as f:
        for line in f:
            m = P_PROFIT.search(line)
            if m:
                bot = m.group(1)
                profit = float(m.group(2))
                bot_profits[bot] += profit
                bot_status[bot] = "active"
                total_profit += profit
            m = P_LATENCY.search(line)
            if m:
                latencies.append(int(m.group(1)))
            if P_MEV.search(line):
                mev_attacks += 1

@app.route("/")
def index():
    process_logs()
    avg_latency = int(sum(latencies)/len(latencies)) if latencies else 0
    active = sum(v=="active" for v in bot_status.values())
    total_bots = len(bot_status)
    html = f"""
    <html><head><meta http-equiv="refresh" content="5"><title>Dashboard</title></head>
    <body style="background:#111;color:#eee;font-family:sans-serif;padding:20px;">
      <h1>🧠 Newland Bot Dashboard</h1>
      <p><strong>Total Profit:</strong> {total_profit:.2f}</p>
      <p><strong>MEV Attacks:</strong> {mev_attacks}</p>
      <p><strong>Average Latency:</strong> {avg_latency} ms</p>
      <p><strong>Active Bots:</strong> {active} / {total_bots}</p>
    </body></html>
    """
    return html

@app.route("/metrics")
def metrics():
    process_logs()
    return jsonify({
        "total_profit": total_profit,
        "mev_attacks": mev_attacks,
        "average_latency": int(sum(latencies)/len(latencies)) if latencies else 0,
        "active_bots": sum(v=="active" for v in bot_status.values()),
        "total_bots": len(bot_status)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
