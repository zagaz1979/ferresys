import io
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from models.venta_model import VentaModel
from models.producto_model import ProductoModel
from models.cliente_model import ClienteModel
from utils.paginator import Paginator


venta_bp = Blueprint("ventas", __name__)


@venta_bp.route("/ventas")
def index():
    search = request.args.get("search", "").strip()
    page = int(request.args.get("page", 1))
    
    todas = VentaModel.get_all(search=search)
    paginacion = Paginator(todas, page=page, per_page=10)
    return render_template("ventas/index.html", paginacion=paginacion, search=search)


@venta_bp.route("/ventas/exportar")
def exportar_excel():
    search = request.args.get("search", "").strip()
    ventas = VentaModel.get_all(search=search)
    
    df = pd.DataFrame(ventas)
    df = df[['id_venta', 'fecha_venta', 'cliente', 'total', 'num_items']]
    df.columns = ['N° Venta', 'Fecha', 'Cliente', 'Total', 'Items']

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Ventas')
    output.seek(0)

    return send_file(output, download_name='ventas.xlsx', as_attachment=True)


@venta_bp.route("/ventas/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        ids = request.form.getlist("id_producto[]")
        cantidades = request.form.getlist("cantidad[]")
        id_cliente = request.form.get("id_cliente") or None

        detalles = []
        for pid, cant in zip(ids, cantidades):
            if not pid or not cant:
                continue
            try:
                cantidad = int(cant)
                if cantidad <= 0:
                    continue
            except ValueError:
                continue
            producto = ProductoModel.get_by_id(int(pid))
            if not producto:
                continue
            if producto["stock"] < cantidad:
                flash(
                    f"Stock insuficiente para '{producto['nombre']}' "
                    f"(disponible: {producto['stock']}).",
                    "danger",
                )
                return redirect(url_for("ventas.crear"))
            detalles.append(
                {
                    "id_producto": int(pid),
                    "cantidad": cantidad,
                    "precio_unitario": float(producto["precio_venta"]),
                }
            )

        if not detalles:
            flash("Debes agregar al menos un producto válido.", "danger")
            return redirect(url_for("ventas.crear"))

        try:
            id_venta = VentaModel.create_venta(detalles, id_cliente)
            flash(f"Venta #{id_venta} registrada correctamente.", "success")
            return redirect(url_for("ventas.detalle", id=id_venta))
        except Exception as e:
            flash(f"Error al registrar la venta: {e}", "danger")
            return redirect(url_for("ventas.crear"))

    productos = ProductoModel.get_all()
    clientes = ClienteModel.get_all()
    return render_template(
        "ventas/crear.html", productos=productos, clientes=clientes
    )


@venta_bp.route("/ventas/<int:id>")
def detalle(id):
    venta = VentaModel.get_by_id(id)
    if not venta:
        flash("Venta no encontrada.", "danger")
        return redirect(url_for("ventas.index"))
    return render_template("ventas/detalle.html", venta=venta)
