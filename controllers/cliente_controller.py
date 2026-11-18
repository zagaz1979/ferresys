from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.cliente_model import ClienteModel

cliente_bp = Blueprint("clientes", __name__)


@cliente_bp.route("/clientes")
def index():
    clientes = ClienteModel.get_all()
    return render_template("clientes/index.html", clientes=clientes)


@cliente_bp.route("/clientes/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if not nombre:
            flash("El nombre es obligatorio.", "danger")
            return redirect(url_for("clientes.crear"))
        data = {
            "nombre": nombre,
            "telefono": request.form.get("telefono", "").strip() or None,
            "email": request.form.get("email", "").strip() or None,
            "direccion": request.form.get("direccion", "").strip() or None,
        }
        try:
            ClienteModel.create(data)
            flash("Cliente registrado.", "success")
            return redirect(url_for("clientes.index"))
        except Exception as e:
            flash(f"Error al registrar cliente: {e}", "danger")
    return render_template("clientes/crear.html")


@cliente_bp.route("/clientes/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    try:
        ClienteModel.delete(id)
        flash("Cliente eliminado.", "danger")
    except Exception as e:
        flash(f"No se pudo eliminar: {e}", "danger")
    return redirect(url_for("clientes.index"))
