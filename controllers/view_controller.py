from flask import Blueprint, render_template, request
from datetime import datetime
from controllers.compare_controller import compare_latest_records
from repositories.json_repository import filter_records


view_bp = Blueprint("view", __name__, template_folder="../templates")


@view_bp.route("/")
def index():
    return render_template("index.html")


@view_bp.route("/registro")
def registro():
    return render_template("registro.html")


@view_bp.route("/registro_usuario")
def registro_usuario():
    return render_template("registro_usuario.html")


@view_bp.route("/login")
def login():
    return render_template("login.html")


@view_bp.route("/api")
def api_view():
    return render_template("api.html")


@view_bp.route("/consulta", methods=["GET", "POST"])
def consulta():
    """
    Muestra el histórico filtrado por municipio y fecha.
    """

    if request.method == "GET":
        registros = filter_records()
        return render_template("consulta.html", registros=registros)

    municipio = request.form.get("municipio", "").strip()

    if not municipio:
        municipio = None

    fecha_raw = request.form.get("fecha", "").strip()
    fecha_formateada = None

    if fecha_raw:
        try:
            fecha_obj = datetime.strptime(fecha_raw, "%Y-%m-%d")
            fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
        except ValueError:
            fecha_formateada = None

    registros = filter_records(
        municipio=municipio,
        fecha=fecha_formateada
    )

    return render_template("consulta.html", registros=registros)


@view_bp.route("/comparar", methods=["GET", "POST"])
def comparar():
    """
    Realiza la comparativa entre JSON y API.
    """

    if request.method == "GET":
        return render_template("comparar.html", resultado=None)

    municipio = request.form.get("municipio", "").strip()
    fecha_html = request.form.get("fecha", "").strip()

    if not municipio:
        return render_template(
            "comparar.html",
            resultado={
                "success": False,
                "message": "Debes introducir un municipio para comparar."
            }
        )

    resultado = compare_latest_records(municipio, fecha_html)

    return render_template("comparar.html", resultado=resultado)