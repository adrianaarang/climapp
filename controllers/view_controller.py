from flask import Flask, render_template, request
from controllers.compare_controller import compare_latest_records
from repositories.json_repository import filter_records

# Creamos la aplicación Flask
app = Flask(__name__)


# Ruta principal opcional
@app.route("/")
def home():
    """
    Muestra la página principal.
    """
    return "<h1>Bienvenida a Climapp</h1>"


# Ruta para comparar registros
@app.route("/comparar", methods=["GET", "POST"])
def comparar():
    """
    Muestra el formulario de comparación y, si el usuario envía un municipio,
    realiza la comparativa entre manual y API AEMET.
    """

    # Si el usuario entra por primera vez en la página,
    # mostramos el HTML sin resultado todavía.
    if request.method == "GET":
        return render_template("comparar.html", resultado=None)

    # Si el usuario ha enviado el formulario (POST),
    # recogemos el municipio escrito.
    municipio = request.form.get("municipio", "").strip()

    # Si no ha escrito nada, devolvemos mensaje de error.
    if not municipio:
        return render_template(
            "comparar.html",
            resultado={
                "success": False,
                "message": "Debes introducir un municipio."
            }
        )

    # Llamamos a tu función de comparativa.
    resultado = compare_latest_records(municipio)

    # Enviamos el resultado al HTML.
    return render_template("comparar.html", resultado=resultado)

# NUEVA RUTA: histórico / consulta
@app.route("/consulta", methods=["GET", "POST"])
def consulta():
    """
    Muestra el histórico de registros y permite filtrar por municipio y fecha.
    """
    # Si entran por primera vez, mostramos todos los registros
    if request.method == "GET":
        registros = filter_records()
        return render_template("consulta.html", registros=registros)

    # Si envían el formulario, recogemos filtros
    municipio = request.form.get("municipio", "").strip()
    fecha = request.form.get("fecha", "").strip()

    # Si algún campo viene vacío, lo convertimos en None
    if not municipio:
        municipio = None

    if not fecha:
        fecha = None

    # Llamamos al repositorio con los filtros
    registros = filter_records(municipio=municipio, fecha=fecha)

    # Enviamos resultados al HTML
    return render_template("consulta.html", registros=registros)





# Esto hace que la aplicación arranque al ejecutar este archivo
if __name__ == "__main__":
    app.run(debug=True)