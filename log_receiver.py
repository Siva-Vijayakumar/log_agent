from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# In-memory log storage
logs = []

# API endpoint to receive logs
@app.route('/logs', methods=['POST'])
def receive_logs():
    data = request.get_json()

    log_entry = {
        "message": data.get("log"),
        "host": data.get("host"),
        "timestamp": data.get("timestamp"),
        "received_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

    logs.append(log_entry)

    return jsonify({"status": "success"}), 200


# Dashboard endpoint
@app.route('/')
@app.route('/dashboard')
def dashboard():

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Log Dashboard</title>
        <meta http-equiv="refresh" content="3">
        <style>
            body {
                font-family: Arial;
                background-color: #0f172a;
                color: #e2e8f0;
                padding: 20px;
            }
            h1 {
                color: #38bdf8;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                border: 1px solid #334155;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #1e293b;
            }
            tr:nth-child(even) {
                background-color: #1e293b;
            }
            .error { color: #ef4444; }
            .warning { color: #facc15; }
            .info { color: #22c55e; }
        </style>
    </head>
    <body>
        <h1>📊 Log Monitoring Dashboard</h1>
        <table>
            <tr>
                <th>Time</th>
                <th>Host</th>
                <th>Message</th>
            </tr>
            {% for log in logs %}
            <tr>
                <td>{{ log.received_at }}</td>
                <td>{{ log.host }}</td>
                <td class="
                    {% if 'ERROR' in log.message %}error
                    {% elif 'WARNING' in log.message %}warning
                    {% else %}info
                    {% endif %}
                ">
                    {{ log.message }}
                </td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(html_template, logs=logs[::-1])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)