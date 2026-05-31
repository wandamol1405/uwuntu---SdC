#!/usr/bin/env python3
import os
import sys
from flask import Flask, render_template_string, jsonify, request

DEVICE_PATH = "/dev/sig_mux"

app = Flask(__name__)

# Variables de control en Flask
tiempo_contador = 0.0  # Lo pasamos a float para manejar pasos decimales en el tiempo
target_canal = 0 
factor_frecuencia_actual = 1  # Guardamos el factor para alterar el paso temporal

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>[SignalMux] - Consola de Sensado Web</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
        text-align: center;
        margin: 0;
        padding: 20px;
    }

    .container {
        width: 90%;
        max-width: 1200px;
        margin: auto;
        background: #111827;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #374151;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }

    .hero { margin-bottom: 20px; }
    .hero h1 { margin: 0; font-size: 42px; color: #00d4ff; }
    .hero h3 { margin: 5px 0; color: #f1c40f; }
    .hero p { color: #bdc3c7; }

    .panel-control {
        background: #1f2937;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }

    button {
        background: linear-gradient(135deg, #2563eb, #06b6d4);
        color: white;
        padding: 12px 24px;
        border: none;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        border-radius: 8px;
        transition: 0.3s;
    }

    button:hover { transform: translateY(-2px); }
    #estado { font-size: 16px; font-weight: bold; }
    .slider-box { display: flex; flex-direction: column; align-items: center; min-width: 200px; }
    .slider-box label { margin-bottom: 8px; color: #d1d5db; font-weight: bold; }
    input[type=range] { width: 100%; }

    .status-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 20px;
    }

    .card {
        background: #1f2937;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 15px;
    }

    .card-title { color: #9ca3af; font-size: 12px; margin-bottom: 5px; }
    .card-value { font-size: 22px; font-weight: bold; }
    #runtime { margin-top: 15px; color: #d1d5db; font-size: 14px; }
</style>
</head>
<body>
    <div class="container">
        <h2>SISTEMA DE ADQUISICIÓN DE SEÑALES VIRTUALES</h2>

        <div class="hero">
            <h1>SignalMux</h1>
            <h3>Grupo UwUntu</h3>
            <p>TP5 - Character Device Driver para Linux</p>
        </div>

        <div class="status-grid">
            <div class="card">
                <div class="card-title">SEÑAL</div>
                <div class="card-value" id="signalName">Senoidal</div>
            </div>
            <div class="card">
                <div class="card-title">AMPLITUD</div>
                <div class="card-value" id="ampDisplay">100</div>
            </div>
            <div class="card">
                <div class="card-title">FRECUENCIA</div>
                <div class="card-value" id="freqDisplay">x1</div>
            </div>
            <div class="card">
                <div class="card-title">DRIVER</div>
                <div class="card-value" id="driverStatus">ONLINE</div>
            </div>
        </div>
        
        <div class="panel-control">
            <div>
                <div id="estado">CONECTANDO AL KERNEL...</div>
                <br>
                <button onclick="conmutar()">CONMUTAR SEÑAL</button>
            </div>
            
            <div class="slider-box">
                <label for="ampSlider">AMPLITUD MÁXIMA: <span id="ampVal">100</span></label>
                <input type="range" id="ampSlider" min="10" max="500" value="100" onchange="cambiarAmplitud(this.value)">
            </div>

            <div class="slider-box">
                <label for="freqSlider">FACTOR FRECUENCIA: <span id="freqVal">1</span>x</label>
                <input type="range" id="freqSlider" min="1" max="5" step="1" value="1" onchange="cambiarFrecuencia(this.value)">
            </div>
        </div>

        <div style="width:100%; height:600px; margin-top:25px;">
            <canvas id="myChart"></canvas>
        </div>

        <div id="runtime">Tiempo de adquisición: 0.0 s</div>
    </div>

    <script>
        let currentCanal = -1; 

        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'Onda Senoidal',
                    data: [],
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52,152,219,0.15)',
                    borderWidth: 3,
                    tension: 0.35,
                    stepped: false,
                    fill: true,
                    pointRadius: 3,
                    pointBackgroundColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                animation: false,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: { display: true, text: 'Amplitud de la Muestra [Unidades Crudas]', color: '#ecf0f1', font: { size: 16 } },
                        ticks: { color: '#bdc3c7' },
                        grid: { color: 'rgba(255,255,255,0.08)' }
                    },
                    y: {
                        type: 'linear',
                        title: { display: true, text: 'Tiempo Físico Transcurrido [s]', color: '#ecf0f1', font: { size: 16 } },
                        ticks: { 
                            color: '#bdc3c7',
                            callback: function(value) { return value.toFixed(1) + ' s'; }
                        },
                        grid: { color: 'rgba(255,255,255,0.08)' }
                    }
                },
                plugins: {
                    legend: { labels: { color: 'white' } }
                }
            }
        });

        async function traerDatos() {
            try {
                let response = await fetch('/data');
                let res = await response.json();

                document.getElementById('driverStatus').innerText = "ONLINE";
                document.getElementById('driverStatus').style.color = "#22c55e";
                
                if (res.status === "error") {
                    document.getElementById('estado').innerText = "ERROR DE LECTURA DEL DRIVER";
                    document.getElementById('estado').style.color = "#ef4444";
                    document.getElementById('driverStatus').innerText = "OFFLINE";
                    document.getElementById('driverStatus').style.color = "#ef4444";
                    return;
                }

                if (res.canal !== currentCanal) {
                    currentCanal = res.canal;
                    myChart.data.datasets[0].data = [];

                    if (currentCanal === 0) {
                        document.getElementById('estado').innerText = "SEÑAL ACTUAL: SENOIDAL";
                        document.getElementById('estado').style.color = "#2ecc71";
                        document.getElementById('signalName').innerText = "Senoidal";
                        myChart.data.datasets[0].label = "Onda Senoidal";
                        myChart.data.datasets[0].borderColor = '#3498db';
                        myChart.data.datasets[0].backgroundColor = 'rgba(52,152,219,0.15)';
                        myChart.data.datasets[0].stepped = false;
                    } else {
                        document.getElementById('estado').innerText = "SEÑAL ACTUAL: CUADRADA";
                        document.getElementById('estado').style.color = "#f1c40f";
                        document.getElementById('signalName').innerText = "Cuadrada";
                        myChart.data.datasets[0].label = "Onda Cuadrada";
                        myChart.data.datasets[0].borderColor = '#e67e22';
                        myChart.data.datasets[0].backgroundColor = 'rgba(230,126,34,0.15)';
                        myChart.data.datasets[0].stepped = 'before';
                    }
                }

                // Agregamos el punto mapeando X (valor) e Y (tiempo físico real)
                myChart.data.datasets[0].data.push({ x: res.valor, y: res.tiempo });

                // Ventana de visualización dinámica de muestras fijas en pantalla
                if (myChart.data.datasets[0].data.length > 50) { 
                    myChart.data.datasets[0].data.shift(); 
                }

                if (myChart.data.datasets[0].data.length > 0) {
                    let puntos = myChart.data.datasets[0].data;
                    let valores = puntos.map(p => p.x);

                    myChart.options.scales.x.min = Math.min(...valores) - 20;
                    myChart.options.scales.x.max = Math.max(...valores) + 20;
                    myChart.options.scales.y.min = puntos[0].y;
                    myChart.options.scales.y.max = puntos[puntos.length - 1].y + 0.5;
                }

                // Actualizamos el cartel del footer del runtime con el tiempo real de adquisición
                document.getElementById('runtime').innerText = "Tiempo de adquisición: " + res.tiempo.toFixed(1) + " s";

                myChart.update();
                
            } catch (error) {
                console.error("Error en adquisición:", error);
            }
        }

        // REDUCIREMOS EL TIEMPO DE LECTURA DE LA WEB A 150ms
        // De esta manera la web va mucho más rápido que el cambio de paso del kernel
        // capturando la resolución sin aliasing.
        setInterval(traerDatos, 150);

        async function conmutar() {
            await fetch('/conmutar', { method: 'POST' });
        }

        async function cambiarAmplitud(valor) {
            document.getElementById('ampVal').innerText = valor;
            document.getElementById('ampDisplay').innerText = valor;
            let formData = new FormData();
            formData.append('amplitud', valor);
            await fetch('/parametro_amplitud', { method: 'POST', body: formData });
        }

        async function cambiarFrecuencia(valor) {
            document.getElementById('freqVal').innerText = valor;
            document.getElementById('freqDisplay').innerText = "x" + valor;
            let formData = new FormData();
            formData.append('frecuencia', valor);
            await fetch('/parametro_frecuencia', { method: 'POST', body: formData });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/data')
def get_data():
    global tiempo_contador, target_canal, factor_frecuencia_actual

    try:
        with open(DEVICE_PATH, "r") as f:
            valor_crudo = int(f.read().strip())

        # SOLUCIÓN DE BASE DE TIEMPO:
        # En vez de sumar 1s fijo, sumamos una fracción basada en los sub-pasos de la LUT.
        # Si la frecuencia es x1 avanzamos lento. Si es x5 avanzamos rápido en el tiempo.
        # El 0.15 calza perfecto con la velocidad del setInterval de la interfaz.
        tiempo_contador += (0.15 * factor_frecuencia_actual)

        return jsonify(
            status="success",
            valor=valor_crudo,
            tiempo=round(tiempo_contador, 2),
            canal=target_canal
        )

    except Exception:
        return jsonify(status="error", msg="Driver desconectado"), 500
    
@app.route('/conmutar', methods=['POST'])
def conmutar_senal():
    global target_canal
    target_canal = 1 if target_canal == 0 else 0
    try:
        with open(DEVICE_PATH, "w") as f:
            f.write(f"C{target_canal}")
        return jsonify(status="success", canal_solicitado=target_canal)
    except Exception as e:
        return jsonify(status="error"), 500

@app.route('/parametro_amplitud', methods=['POST'])
def parametro_amplitud():
    amplitud = request.form.get('amplitud', 100)
    try:
        with open(DEVICE_PATH, "w") as f:
            f.write(f"A{amplitud}")
        return jsonify(status="success")
    except Exception as e:
        return jsonify(status="error"), 500

@app.route('/parametro_frecuencia', methods=['POST'])
def parametro_frecuencia():
    global factor_frecuencia_actual
    frecuencia = request.form.get('frecuencia', 1)
    try:
        factor_frecuencia_actual = int(frecuencia)
        with open(DEVICE_PATH, "w") as f:
            f.write(f"F{frecuencia}")
        return jsonify(status="success")
    except Exception:
        return jsonify(status="error"), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)