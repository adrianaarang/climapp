from flask import Blueprint, render_template, request
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
    return render_template("api.html")

@view_bp.route("/consulta", methods=["GET", "POST"])
def consulta():
    """
    Muestra el histórico. 
    RETOQUE INTEGRACIÓN: Manejamos tanto si filter_records devuelve lista como diccionario.
    """
    municipio = None
    fecha = None

    if request.method == "POST":
        municipio = request.form.get("municipio", "").strip().upper()
        fecha = request.form.get("fecha", "").strip()

    # Llamada al repositorio
    respuesta = filter_records(municipio=municipio if municipio else None, fecha=fecha if fecha else None)
    
    # SOLUCIÓN AL ERROR: Comprobamos el tipo de dato recibido
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
    Bridge para conectar el Dashboard con los datos de Elena (AEMET) o Isabela (JSON).
    """
    municipio_actual = request.args.get('municipio', "MADRID").strip().upper()
    
    try:
        resultado = compare_latest_records(municipio_actual)
        
        # 1. Si no hay datos de Elena/AEMET, buscamos en el repositorio local
        if not resultado or not resultado.get("success"):
            respuesta_repo = filter_records(municipio=municipio_actual)
            
            # Verificamos si es lista o dict
            if isinstance(respuesta_repo, dict):
                registros = respuesta_repo.get("data", [])
            else:
                registros = respuesta_repo 
            
            datos = registros[0] if registros else {}
            
            return {
                "success": True if datos else False,
                "temperatura": float(datos.get("temperatura", 0)),
                "humedad": float(datos.get("humedad", 0)),
                "viento": float(datos.get("viento", 0)),
                "lluvia": float(datos.get("lluvia", 0)),
                "estacion": datos.get("estacion_id", "SIN DATOS RECIENTES"),
                "municipio": municipio_actual,
                "fecha": datetime.now().isoformat()
            }, 200

        # 2. Si Elena tiene éxito, normalizamos su respuesta (soporta varios formatos de clave)
        fuente = resultado.get("aemet") or resultado.get("manual") or {}
        
        temp = fuente.get("temperatura") or fuente.get("temp") or 0
        hum  = fuente.get("humedad") or fuente.get("hr") or 0
        vnt  = fuente.get("viento") or fuente.get("vv") or 0
        pre  = fuente.get("lluvia") or fuente.get("prec") or 0

        return {
            "success": True,
            "temperatura": float(temp),
            "humedad": float(hum),
            "viento": float(vnt),
            "lluvia": float(pre),
            "estacion": fuente.get("estacion_id", "AEMET OFICIAL"),
            "municipio": municipio_actual,
            "fecha": datetime.now().isoformat()
        }, 200

    except Exception as e:
        print(f"Error crítico en bridge: {e}")
        return {
            "success": False, 
            "municipio": municipio_actual, 
            "fecha": datetime.now().isoformat(),
            "error": str(e)
        }, 200