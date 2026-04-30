from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import os

# Blueprints
from controllers.view_controller import view_bp
from controllers.manual_controller import manual_bp
from controllers.auth_controller import auth_bp
from controllers.compare_controller import compare_latest_records

# Servicios
from services.weather_api_service import obtener_clima_por_coordenadas
from services.normalizer_service import normalizar_datos_aemet

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clave_secreta")


# --- MIGAS DE PAN ---
def generar_migas():
    path = request.path.strip("/").split("/")
    migas = [{"text": "Inicio", "url": "/"}]

    acumulado = ""

    for segmento in path:
        if segmento:
            acumulado += f"/{segmento}"
            migas.append({
                "text": segmento.replace("_", " ").capitalize(),
                "url": acumulado
            })

    return migas


@app.context_processor
def inject_vars():
    return dict(breadcrumbs=generar_migas())


# --- REGISTRO DE BLUEPRINTS ---
app.register_blueprint(view_bp)
app.register_blueprint(manual_bp)
app.register_blueprint(auth_bp)


# --- RUTA COMPARAR ---
@app.route("/comparar", methods=["GET", "POST"])
def comparar():
    resultado = None

    if request.method == "POST":
        municipio = request.form.get("municipio")
        fecha_html = request.form.get("fecha")

        print("Municipio recibido:", municipio)
        print("Fecha recibida:", fecha_html)

        resultado = compare_latest_records(municipio, fecha_html)

    return render_template("comparar.html", resultado=resultado)


# --- API CLIMA ---
@app.route("/api/clima")
def api_clima():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Faltan coordenadas"}), 400

    try:
        raw_data = obtener_clima_por_coordenadas(lat, lon)
        data_normalizada = normalizar_datos_aemet(raw_data)

        return jsonify(data_normalizada), 200

    except Exception as e:
        print(f"Error en /api/clima: {e}")
        return jsonify({"error": str(e)}), 500


# --- INICIO APP ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)