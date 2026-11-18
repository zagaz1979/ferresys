import io
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from models.producto_model import ProductoModel
from models.categoria_model import CategoriaModel
from utils.paginator import Paginator


producto_bp = Blueprint("productos", __name__)


def _parse_producto_form():
    """Valida y devuelve el diccionario de datos del formulario de producto."""
    try:
        data = {
            "codigo_barras": request.form["codigo_barras"].strip(),
            "nombre": request.form["nombre"].strip(),
            "precio_compra": float(request.form["precio_compra"]),
            "precio_venta": float(request.form["precio_venta"]),
            "stock": int(request.form["stock"]),
            "stock_minimo": int(request.form["stock_minimo"]),
            "id_categoria": request.form.get("id_categoria") or None,
        }
    except (KeyError, ValueError) as e:
        raise ValueError(f"Datos inválidos en el formulario: {e}")

    if not data["codigo_barras"] or not data["nombre"]:
        raise ValueError("Código y nombre son obligatorios.")
    if data["precio_compra"] < 0 or data["precio_venta"] < 0:
        raise ValueError("Los precios no pueden ser negativos.")
    if data["stock"] < 0 or data["stock_minimo"] < 0:
        raise ValueError("El stock no puede ser negativo.")
    return data


@producto_bp.route("/productos")
def index():
    search = request.args.get("search", "").strip()
    page = int(request.args.get("page", 1))
    
    todos = ProductoModel.get_all(search=search)
    paginacion = Paginator(todos, page=page, per_page=10) # 10 por página
    
    return render_template("productos/index.html", paginacion=paginacion, search=search)


@producto_bp.route("/productos/exportar")
def exportar_excel():
    search = request.args.get("search", "").strip()
    productos = ProductoModel.get_all(search=search)
    
    if not productos:
        flash("No hay datos para exportar.", "warning")
        return redirect(url_for("productos.index"))

    # Crear DataFrame
    df = pd.DataFrame(productos)
    # Seleccionar y renombrar columnas
    df = df[['codigo_barras', 'nombre', 'categoria', 'precio_compra', 'precio_venta', 'stock']]
    df.columns = ['Código', 'Nombre', 'Categoría', 'P. Compra', 'P. Venta', 'Stock']

    # Guardar en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Productos')
    output.seek(0)

    return send_file(output, download_name='productos.xlsx', as_attachment=True)


@producto_bp.route("/productos/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        try:
            data = _parse_producto_form()
            ProductoModel.create(data)
            flash("Producto registrado correctamente.", "success")
            return redirect(url_for("productos.index"))
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for("productos.crear"))
    categorias = CategoriaModel.get_all()
    return render_template("productos/crear.html", categorias=categorias)


@producto_bp.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    producto = ProductoModel.get_by_id(id)
    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("productos.index"))

    if request.method == "POST":
        try:
            data = _parse_producto_form()
            ProductoModel.update(id, data)
            flash("Producto actualizado correctamente.", "success")
            return redirect(url_for("productos.index"))
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for("productos.editar", id=id))

    categorias = CategoriaModel.get_all()
    return render_template(
        "productos/editar.html", producto=producto, categorias=categorias
    )


@producto_bp.route("/productos/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    try:
        ProductoModel.delete(id)
        flash("Producto eliminado.", "danger")
    except Exception as e:
        flash(f"No se pudo eliminar el producto: {e}", "danger")
    return redirect(url_for("productos.index"))
