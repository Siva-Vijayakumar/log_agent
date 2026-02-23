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
        <title>Advanced Log Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: #0f172a;
                color: #e2e8f0;
                margin: 0;
                padding: 20px;
            }

            h1 {
                text-align: center;
                color: #38bdf8;
            }

            .stats {
                display: flex;
                gap: 20px;
                justify-content: center;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }

            .card {
                background: #1e293b;
                padding: 20px;
                border-radius: 10px;
                width: 200px;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0,0,0,0.4);
            }

            .card h2 {
                margin: 0;
                font-size: 28px;
            }

            .chart-container {
                width: 60%;
                margin: auto;
                margin-bottom: 40px;
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

        <h1>📊 Advanced Log Monitoring Dashboard</h1>

        <div class="stats">
            <div class="card">
                <h3>Total Logs</h3>
                <h2 id="totalLogs">0</h2>
            </div>
            <div class="card">
                <h3>Errors</h3>
                <h2 id="errorCount">0</h2>
            </div>
            <div class="card">
                <h3>Warnings</h3>
                <h2 id="warningCount">0</h2>
            </div>
            <div class="card">
                <h3>Info</h3>
                <h2 id="infoCount">0</h2>
            </div>
        </div>

        <div class="chart-container">
            <canvas id="logChart"></canvas>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Host</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody id="logTable"></tbody>
        </table>

        <script>
            let chart;

            async function fetchLogs() {
                const response = await fetch('/api/logs');
                const logs = await response.json();

                const table = document.getElementById("logTable");
                table.innerHTML = "";

                let error = 0, warning = 0, info = 0;

                logs.forEach(log => {
                    let row = document.createElement("tr");

                    let levelClass = "info";
                    if (log.message.includes("ERROR")) {
                        error++;
                        levelClass = "error";
                    } else if (log.message.includes("WARNING")) {
                        warning++;
                        levelClass = "warning";
                    } else {
                        info++;
                    }

                    row.innerHTML = `
                        <td>${log.received_at}</td>
                        <td>${log.host}</td>
                        <td class="${levelClass}">${log.message}</td>
                    `;
                    table.appendChild(row);
                });

                document.getElementById("totalLogs").innerText = logs.length;
                document.getElementById("errorCount").innerText = error;
                document.getElementById("warningCount").innerText = warning;
                document.getElementById("infoCount").innerText = info;

                updateChart(error, warning, info);
            }

            function updateChart(error, warning, info) {
                if (chart) chart.destroy();

                const ctx = document.getElementById('logChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Errors', 'Warnings', 'Info'],
                        datasets: [{
                            data: [error, warning, info],
                            backgroundColor: ['#ef4444', '#facc15', '#22c55e']
                        }]
                    }
                });
            }

            fetchLogs();
            setInterval(fetchLogs, 3000);
        </script>

    </body>
    </html>
    """

    return render_template_string(html_template, logs=logs[::-1])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)