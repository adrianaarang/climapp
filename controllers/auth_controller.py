import json
import os
import re
import hashlib

from flask import Blueprint, request, redirect, url_for, session, flash
from models.usuario import Usuario


auth_bp = Blueprint("auth", __name__)


class AuthController:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, "data")
        self.data_path = os.path.join(self.data_dir, "usuarios.json")

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def encriptar_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def cargar_usuarios(self):
        if not os.path.exists(self.data_path):
            return []

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def guardar_usuarios(self, usuarios):
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)

    def validar_datos(self, email, password):
        regex_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(regex_email, email):
            return False, "El formato del email no es válido."

        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."

        return True, ""

    def registrar_usuario(self, email, password):
        valido, mensaje = self.validar_datos(email, password)

        if not valido:
            return False, mensaje

        usuarios = self.cargar_usuarios()

        for usuario in usuarios:
            if usuario["email"] == email:
                return False, "Este correo ya está registrado."

        password_encriptada = self.encriptar_password(password)

        nuevo_usuario = Usuario(email, password_encriptada)
        usuarios.append(nuevo_usuario.to_dict())

        self.guardar_usuarios(usuarios)

        return True, "Registro completado con éxito."

    def iniciar_sesion(self, email, password):
        usuarios = self.cargar_usuarios()
        password_encriptada = self.encriptar_password(password)

        for usuario in usuarios:
            if usuario["email"] == email and usuario["password"] == password_encriptada:
                return True, "Login correcto."

        return False, "Email o contraseña incorrectos."


auth_controller = AuthController()


@auth_bp.route("/registro_usuario", methods=["POST"])
def registrar_usuario():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    confirm_password = request.form.get("confirm_password", "").strip()

    if password != confirm_password:
        flash("Las contraseñas no coinciden.", "error")
        return redirect(url_for("view.registro_usuario"))

    exito, mensaje = auth_controller.registrar_usuario(email, password)

    if exito:
        flash(mensaje, "success")
        return redirect(url_for("view.login"))

    flash(mensaje, "error")
    return redirect(url_for("view.registro_usuario"))


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    exito, mensaje = auth_controller.iniciar_sesion(email, password)

    if exito:
        session["usuario"] = email
        flash(mensaje, "success")
        return redirect(url_for("view.index"))

    flash(mensaje, "error")
    return redirect(url_for("view.login"))


@auth_bp.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("view.index"))