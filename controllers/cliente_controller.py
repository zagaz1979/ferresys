import io
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from models.cliente_model import ClienteModel
from utils.paginator import Paginator


cliente_bp = Blueprint("clientes", __name__)


@cliente_bp.route("/clientes")
def index():
    search = request.args.get("search", "").strip()
    page = int(request.args.get("page", 1))
    
    todos = ClienteModel.get_all(search=search)
    paginacion = Paginator(todos, page=page, per_page=10)
    return render_template("clientes/index.html", paginacion=paginacion, search=search)


@cliente_bp.route("/clientes/exportar")
def exportar_excel():
    search = request.args.get("search", "").strip()
    clientes = ClienteModel.get_all(search=search)
    
    df = pd.DataFrame(clientes)
    df = df[['id_cliente', 'nombre', 'telefono', 'email', 'direccion']]
    df.columns = ['ID', 'Nombre', 'Teléfono', 'Email', 'Dirección']

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Clientes')
    output.seek(0)

    return send_file(output, download_name='clientes.xlsx', as_attachment=True)


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
