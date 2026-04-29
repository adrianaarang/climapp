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
    # 1. Normalizamos el municipio para que Elena lo encuentre
    municipio_actual = request.args.get('municipio', "MADRID").strip().upper()
    
    try:
        resultado = compare_latest_records(municipio_actual)
        
        # 1. Si falla Elena, vamos al repositorio de Isabela
        if not resultado or not resultado.get("success"):
            respuesta_repo = filter_records(municipio=municipio_actual)
            
            # Verificamos si es lista (nuevo formato) o dict (formato antiguo)
            if isinstance(respuesta_repo, dict):
                registros = respuesta_repo.get("data", [])
            else:
                registros = respuesta_repo # Ya es una lista
            
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

        # 2. Si Elena tiene éxito, usamos su resultado (AEMET/Manual)
        fuente = resultado.get("aemet") or resultado.get("manual") or {}
        return {
            "success": True,
            "temperatura": float(fuente.get("temperatura", fuente.get("temp", 0))),
            "humedad": float(fuente.get("humedad", fuente.get("hr", 0))),
            "viento": float(fuente.get("viento", fuente.get("vv", 0))),
            "lluvia": float(fuente.get("lluvia", fuente.get("prec", 0))),
            "estacion": fuente.get("estacion_id", "AEMET OFICIAL"),
            "municipio": municipio_actual,
            "fecha": datetime.now().isoformat()
        }, 200

    except Exception as e:
        print(f"Error de compatibilidad detectado: {e}")
        return {"success": False, "municipio": municipio_actual, "fecha": datetime.now().isoformat()}, 200

        # 2. Buscamos los datos en AEMET o Manual
        fuente = resultado.get("aemet") or resultado.get("manual") or {}
        
        # REFUERZO: Elena a veces anida los datos. Si 'fuente' está vacía o 
        # no tiene temperatura, buscamos un nivel más abajo si existe.
        temp = fuente.get("temperatura") or fuente.get("temp") or 0
        hum  = fuente.get("humedad") or fuente.get("hr") or 0
        vnt  = fuente.get("viento") or fuente.get("vv") or 0
        pre  = fuente.get("lluvia") or fuente.get("prec") or 0

        # 3. Formateo de fecha: JS ama el formato ISO
        return {
            "success": True,
                "temperatura": float(temp), # Aseguramos que sea número
                "humedad":     float(hum),
                "viento":      float(vnt),
                "lluvia":      float(pre),
            "estacion":    fuente.get("estacion_id") or "AEMET OFICIAL",
            "municipio":   resultado.get("municipio") or municipio_actual,
            "fecha":       datetime.now().isoformat() 
        }, 200

    except Exception as e:
        print(f"Error crítico: {e}")
        return {"success": False, "fecha": datetime.now().isoformat()}, 200