from flask import Flask
import os

app = Flask(__name__)

LOG_FILE = "/app/logs/metrics.log"


@app.route("/")
def dashboard():
    if not os.path.exists(LOG_FILE):
        return "<h1>Log Monitor</h1><p>No logs yet. Waiting for data...</p>"

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    last_50 = lines[-50:]
    log_html = "<br>".join(line.strip() for line in reversed(last_50))

    html = (
        "<html>"
        "<head><title>Log Monitor</title>"
        "<style>"
        "body { background: #0d1117; color: #c9d1d9; font-family: monospace; padding: 20px; }"
        "h1 { color: #58a6ff; }"
        ".logs { background: #161b22; padding: 20px; border-radius: 8px; line-height: 1.8; }"
        "</style>"
        '<meta http-equiv="refresh" content="10">'
        "</head>"
        "<body>"
        "<h1>System Log Monitor</h1>"
        "<p>Auto-refreshes every 10 seconds. Showing last 50 entries.</p>"
        '<div class="logs">' + log_html + "</div>"
        "</body>"
        "</html>"
    )

    return html


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)