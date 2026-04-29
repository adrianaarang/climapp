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
    RETOQUE INTEGRACIÓN: Extraemos la lista de la clave 'data' que envía Isabela.
    """
    if request.method == "GET":
        # Llamada inicial: obtenemos el diccionario y extraemos la lista
        respuesta = filter_records()
        registros = respuesta.get("data", [])
        return render_template("consulta.html", registros=registros)

    # Filtrado por formulario
    municipio = request.form.get("municipio", "").strip().upper()
    fecha = request.form.get("fecha", "").strip()
    
    # Llamada con filtros: extraemos de nuevo la lista real
    respuesta = filter_records(municipio=municipio if municipio else None, fecha=fecha if fecha else None)
    registros = respuesta.get("data", [])
    
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
    PUENTE NINJA EVOLUCIONADO:
    Soporta coordenadas y normaliza llaves técnicas de AEMET.
    """
    municipio_actual = request.args.get('municipio', "MADRID").strip().upper()
    
    try:
        resultado = compare_latest_records(municipio_actual)
        
        if not resultado or not resultado.get("success"):
            return {
                "success": False,
                "temperatura": 0, "humedad": 0, "viento": 0, "lluvia": 0,
                "estacion": "Buscando...", "municipio": municipio_actual,
                "fecha": datetime.now().strftime("%H:%M:%S")
            }, 200

        fuente = resultado.get("aemet") or resultado.get("manual") or {}
        
        temp = fuente.get("temperatura") or fuente.get("temp") or 0
        hum = fuente.get("humedad") or fuente.get("hr") or 0
        vnt = fuente.get("viento") or fuente.get("vv") or 0
        prec = fuente.get("lluvia") or fuente.get("prec") or 0

        fecha_final = fuente.get("fecha")
        if not fecha_final or fecha_final == "--":
            fecha_final = datetime.now().strftime("%H:%M:%S")

        return {
            "success": True,
            "temperatura": temp,
            "humedad":     hum,
            "viento":      vnt,
            "lluvia":      prec,
            "estacion":    fuente.get("estacion_id") or "MADRID RETIRO",
            "municipio":   resultado.get("municipio") or municipio_actual,
            "fecha":       fecha_final
        }, 200

    except Exception as e:
        print(f"Error en el puente: {e}")
        return {"success": False, "temperatura": 0, "fecha": "--:--"}, 200