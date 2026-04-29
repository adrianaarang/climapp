from flask import Blueprint, render_template, request, jsonify
from controllers.compare_controller import compare_latest_records
from repositories.json_repository import filter_records
from datetime import datetime

view_bp = Blueprint("view", __name__, template_folder="../templates")

@view_bp.route("/")
def index():
    return render_template("index.html")

@view_bp.route("/registro")
def registro():
    return render_template("registro.html")

@view_bp.route("/api")
def api_view():
    """
    CORRECCIÓN: El botón API del menú ahora carga el Dashboard real.
    """
    return render_template("index.html")

@view_bp.route("/consulta", methods=["GET", "POST"])
def consulta():
    municipio = None
    fecha = None

    if request.method == "POST":
        municipio = request.form.get("municipio", "").strip().upper()
        fecha = request.form.get("fecha", "").strip()

    respuesta = filter_records(municipio=municipio if municipio else None, fecha=fecha if fecha else None)
    
    if isinstance(respuesta, dict):
        registros = respuesta.get("data", [])
    elif isinstance(respuesta, list):
        registros = respuesta
    else:
        registros = []

    return render_template("consulta.html", registros=registros)

@view_bp.route("/comparar", methods=["GET", "POST"])
def comparar():
    if request.method == "GET":
        return render_template("comparar.html", resultado=None)

    municipio = request.form.get("municipio", "").strip().upper()
    if not municipio:
        return render_template("comparar.html", resultado={"success": False, "message": "Debes introducir un municipio."})

    resultado = compare_latest_records(municipio)
    return render_template("comparar.html", resultado=resultado)

@view_bp.route("/api/clima")
def api_clima_bridge():
    """
    Bridge optimizado: Devuelve JSON puro para que index.js lo procese.
    """
    # Intentamos obtener lat/lon primero, si no, usamos el municipio por defecto
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    municipio_actual = request.args.get('municipio', "MADRID").strip().upper()
    
    try:
        # Llamamos a la lógica de comparación/obtención de datos
        resultado = compare_latest_records(municipio_actual)
        
        # 1. Fallback: Si la API externa falla, tiramos del historial local
        if not resultado or not resultado.get("success"):
            respuesta_repo = filter_records(municipio=municipio_actual)
            registros = respuesta_repo.get("data", []) if isinstance(respuesta_repo, dict) else respuesta_repo
            datos = registros[0] if registros else {}
            
            return jsonify({
                "success": True if datos else False,
                "temperatura": float(datos.get("temperatura", 0)),
                "humedad": float(datos.get("humedad", 0)),
                "viento": float(datos.get("viento", 0)),
                "lluvia": float(datos.get("lluvia", 0)),
                "estacion": datos.get("estacion_id", "SIN DATOS RECIENTES"),
                "municipio": municipio_actual,
                "fecha": datetime.now().isoformat()
            })

        # 2. Éxito: Normalizamos la fuente (AEMET o Manual)
        fuente = resultado.get("aemet") or resultado.get("manual") or {}
        
        return jsonify({
            "success": True,
            "temperatura": float(fuente.get("temperatura") or fuente.get("temp") or 0),
            "humedad": float(fuente.get("humedad") or fuente.get("hr") or 0),
            "viento": float(fuente.get("viento") or fuente.get("vv") or 0),
            "lluvia": float(fuente.get("lluvia") or fuente.get("prec") or 0),
            "estacion": fuente.get("estacion_id", "AEMET OFICIAL"),
            "municipio": municipio_actual,
            "fecha": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e),
            "municipio": municipio_actual,
            "fecha": datetime.now().isoformat()
        }), 500