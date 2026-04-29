from flask import Blueprint, render_template, request
from controllers.compare_controller import compare_latest_records
from repositories.json_repository import filter_records

# Blueprint para las vistas - Mantenemos la estructura de carpetas original
view_bp = Blueprint("view", __name__, template_folder="../templates")

@view_bp.route("/")
def index():
    """Vista principal: Dashboard."""
    return render_template("index.html")

@view_bp.route("/registro")
def registro():
    """Vista de registro manual de datos."""
    return render_template("registro.html")

@view_bp.route("/api")
def api_view():
    """Vista de visualización de datos de la API."""
    return render_template("api.html")

@view_bp.route("/consulta", methods=["GET", "POST"])
def consulta():
    """
    Muestra el histórico de registros y permite filtrar por municipio y fecha.
    Implementado por Elena.
    """
    if request.method == "GET":
        registros = filter_records()
        return render_template("consulta.html", registros=registros)

    municipio = request.form.get("municipio", "").strip()
    fecha = request.form.get("fecha", "").strip()

    # Normalización para el repositorio respetando la lógica de Elena
    municipio_query = municipio if municipio else None
    fecha_query = fecha if fecha else None

    registros = filter_records(municipio=municipio_query, fecha=fecha_query)
    return render_template("consulta.html", registros=registros)

@view_bp.route("/comparar", methods=["GET", "POST"])
def comparar():
    """
    Realiza la comparativa manual vs AEMET.
    Implementado por Elena.
    """
    if request.method == "GET":
        return render_template("comparar.html", resultado=None)

    municipio = request.form.get("municipio", "").strip()

    if not municipio:
        return render_template(
            "comparar.html",
            resultado={
                "success": False,
                "message": "Debes introducir un municipio."
            }
        )

    # Llamada directa al controlador de Elena
    resultado = compare_latest_records(municipio)
    return render_template("comparar.html", resultado=resultado)

@view_bp.route("/api/clima")
def api_clima_bridge():
    """
    ADAPTADOR DE INTEGRACIÓN (Puente Ninja):
    Mapea el objeto complejo de Elena al formato plano que espera el JS de Adriana.
    Resuelve NaN (asegurando números) y undefined (mapeando llaves).
    """
    municipio_por_defecto = "Madrid"
    
    try:
        # 1. CAPTURA: Usamos el motor de Elena sin modificarlo.
        # Intentamos obtener el municipio de la URL, si no, usamos el de por defecto.
        municipio_actual = request.args.get('municipio', municipio_por_defecto)
        resultado = compare_latest_records(municipio_actual)
        
        # 2. VERIFICACIÓN: Si la lógica de Elena indica fallo, enviamos ceros para no romper el JS.
        if not resultado or not resultado.get("success"):
            return {
                "success": False,
                "temperatura": 0, 
                "humedad": 0, 
                "viento": 0, 
                "lluvia": 0,
                "estacion": "Sin datos", 
                "municipio": municipio_actual
            }, 200

        # 3. EXTRACCIÓN: Elena anida los datos en 'aemet' o 'manual'.
        # Adriana busca los datos en la raíz del objeto.
        datos_fuente = resultado.get("aemet") or resultado.get("manual") or {}

        # 4. MAPEO FINAL (Traducción):
        # Mapeamos 'estacion_id' -> 'estacion' (Adriana's JS)
        # Aseguramos que los valores sean numéricos para evitar NaN.
        return {
            "success": True,
            "temperatura": datos_fuente.get("temperatura", 0),
            "humedad":     datos_fuente.get("humedad", 0),
            "viento":      datos_fuente.get("viento", 0),
            "lluvia":      datos_fuente.get("lluvia", 0),
            "estacion":    datos_fuente.get("estacion_id") or resultado.get("municipio") or "Estación AEMET",
            "municipio":   resultado.get("municipio") or municipio_actual,
            "fecha":       datos_fuente.get("fecha", "--")
        }, 200

    except Exception as e:
        # Log para trazabilidad en consola
        print(f"Error crítico de integración en DashLogistics: {e}")
        # Fallback de seguridad total (Garantiza que la UI no se bloquee)
        return {
            "success": False,
            "temperatura": 0, 
            "humedad": 0, 
            "viento": 0, 
            "lluvia": 0,
            "estacion": "Error", 
            "municipio": "Error"
        }, 200