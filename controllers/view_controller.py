from flask import Blueprint, render_template

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

# Esta es la ruta crítica: Mantenemos el nombre 'consulta' para que url_for('view.consulta') no falle
@view_bp.route("/historico")
def consulta():
    return render_template("consulta.html")

@view_bp.route("/comparar")
def comparar():
    return render_template("comparar.html")