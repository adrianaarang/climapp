from flask import Flask, request
from dotenv import load_dotenv
import os

# 1. IMPORTACIÓN DE BLUEPRINTS
from controllers.view_controller import view_bp
from controllers.manual_controller import manual_bp
from controllers.auth_controller import auth_bp
from controllers.api_controller import api_bp

# 2. IMPORTACIÓN DEL SCHEDULER (Tareas automáticas)
from controllers.scheduler_controller import init_scheduler

# Cargar variables de entorno (.env)
load_dotenv()

app = Flask(__name__)

# Configuración básica
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clave_secreta")

# --- CONTEXT PROCESSOR (Migas de pan) ---
# Esto permite usar la variable 'breadcrumbs' en cualquier archivo HTML
@app.context_processor
def inject_vars():
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
    return dict(breadcrumbs=migas)

# --- REGISTRO DE BLUEPRINTS ---
# Conectamos todos los archivos de la carpeta controllers
app.register_blueprint(view_bp)    # Páginas HTML (index, consulta...)
app.register_blueprint(manual_bp)  # Registro manual de datos
app.register_blueprint(auth_bp)    # Login y registro de usuarios
app.register_blueprint(api_bp)     # API de clima (GPS / AEMET)

# --- INICIALIZAR TAREAS AUTOMÁTICAS ---
# Esto hará que el servidor pida datos a AEMET por su cuenta cada X tiempo
try:
    init_scheduler(app)
except Exception as e:
    print(f"⚠️ No se pudo iniciar el scheduler: {e}")

# --- EJECUCIÓN DEL SERVIDOR ---
if __name__ == "__main__":
    # debug=True: el servidor se reinicia solo al detectar cambios en el código
    # host="0.0.0.0": permite que otros dispositivos en tu red vean la web
    app.run(debug=True, host="0.0.0.0", port=5000)