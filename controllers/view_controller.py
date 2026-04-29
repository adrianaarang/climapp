from flask import Blueprint, render_template, request
from controllers.compare_controller import compare_latest_records
from repositories.json_repository import filter_records

# Blueprint para las vistas
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
    Muestra el histórico de registros y permite filtrar por municipio y fecha.
    Implementado por Elena 
    """
    if request.method == "GET":
        registros = filter_records()
        return render_template("consulta.html", registros=registros)

    municipio = request.form.get("municipio", "").strip()
    fecha = request.form.get("fecha", "").strip()

    # Normalización para el repositorio
    municipio_query = municipio if municipio else None
    fecha_query = fecha if fecha else None

    registros = filter_records(municipio=municipio_query, fecha=fecha_query)
    return render_template("consulta.html", registros=registros)

@view_bp.route("/comparar", methods=["GET", "POST"])
def comparar():
    """
    Realiza la comparativa manual vs AEMET.
    Implementado por Elena 
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

    resultado = compare_latest_records(municipio)
    return render_template("comparar.html", resultado=resultado)