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
    """

    if request.method == "GET":
        registros = filter_records()
        return render_template("consulta.html", registros=registros)

    municipio = request.form.get("municipio", "").strip()
    fecha = request.form.get("fecha", "").strip()

    if not municipio:
        municipio = None

    if not fecha:
        fecha = None

    registros = filter_records(municipio=municipio, fecha=fecha)

    return render_template("consulta.html", registros=registros)


@view_bp.route("/comparar", methods=["GET", "POST"])
def comparar():
    """
    Muestra el formulario de comparación y realiza la comparativa.
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