from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registro")
def registro():
    return render_template("registro.html")


@app.route("/api")
def api():
    return render_template("api.html")


@app.route("/consulta")
def consulta():
    return render_template("consulta.html")


@app.route("/comparar")
def comparar():
    return render_template("comparar.html")




if __name__ == "__main__":
    app.run(debug=True)