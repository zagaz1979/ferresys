from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.categoria_model import CategoriaModel

categoria_bp = Blueprint("categorias", __name__)


@categoria_bp.route("/categorias")
def index():
    categorias = CategoriaModel.get_all()
    return render_template("categorias/index.html", categorias=categorias)


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
