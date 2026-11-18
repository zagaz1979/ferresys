import io
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from models.categoria_model import CategoriaModel
from utils.paginator import Paginator


categoria_bp = Blueprint("categorias", __name__)


@categoria_bp.route("/categorias")
def index():
    search = request.args.get("search", "").strip()
    page = int(request.args.get("page", 1))
    
    todos = CategoriaModel.get_all(search=search)
    paginacion = Paginator(todos, page=page, per_page=10)
    return render_template("categorias/index.html", paginacion=paginacion, search=search)


@categoria_bp.route("/categorias/exportar")
def exportar_excel():
    search = request.args.get("search", "").strip()
    categorias = CategoriaModel.get_all(search=search)
    
    df = pd.DataFrame(categorias)
    df = df[['id_categoria', 'nombre', 'descripcion']]
    df.columns = ['ID', 'Nombre', 'Descripción']

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Categorias')
    output.seek(0)

    return send_file(output, download_name='categorias.xlsx', as_attachment=True)


@categoria_bp.route("/categorias/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip() or None
        if not nombre:
            flash("El nombre es obligatorio.", "danger")
            return redirect(url_for("categorias.crear"))
        try:
            CategoriaModel.create({"nombre": nombre, "descripcion": descripcion})
            flash("Categoría creada correctamente.", "success")
            return redirect(url_for("categorias.index"))
        except Exception as e:
            flash(f"Error al crear categoría: {e}", "danger")
    return render_template("categorias/crear.html")


@categoria_bp.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    categoria = CategoriaModel.get_by_id(id)
    if not categoria:
        flash("Categoría no encontrada.", "danger")
        return redirect(url_for("categorias.index"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip() or None
        if not nombre:
            flash("El nombre es obligatorio.", "danger")
            return redirect(url_for("categorias.editar", id=id))
        try:
            CategoriaModel.update(
                id, {"nombre": nombre, "descripcion": descripcion}
            )
            flash("Categoría actualizada.", "success")
            return redirect(url_for("categorias.index"))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")
    return render_template("categorias/editar.html", categoria=categoria)


@categoria_bp.route("/categorias/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    try:
        CategoriaModel.delete(id)
        flash("Categoría eliminada.", "danger")
    except Exception as e:
        flash(f"No se pudo eliminar: {e}", "danger")
    return redirect(url_for("categorias.index"))
