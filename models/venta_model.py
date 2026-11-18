from config import get_db_connection


class VentaModel:

    @staticmethod
    def create_venta(detalles, id_cliente=None):
        """
        Crea una venta transaccional.
        detalles: lista de dicts {'id_producto', 'cantidad', 'precio_unitario'}
        Retorna el id_venta generado.
        """
        if not detalles:
            raise ValueError("La venta debe tener al menos un producto.")

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                total = round(
                    sum(d["cantidad"] * d["precio_unitario"] for d in detalles), 2
                )

                # Insertar cabecera
                cursor.execute(
                    "INSERT INTO ventas (total, id_cliente) VALUES (%s, %s)",
                    (total, id_cliente),
                )
                id_venta = cursor.lastrowid

                # Insertar detalles y descontar stock
                for d in detalles:
                    subtotal = round(d["cantidad"] * d["precio_unitario"], 2)
                    cursor.execute(
                        """INSERT INTO detalle_ventas
                           (id_venta, id_producto, cantidad, precio_unitario, subtotal)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (
                            id_venta,
                            d["id_producto"],
                            d["cantidad"],
                            d["precio_unitario"],
                            subtotal,
                        ),
                    )
                    cursor.execute(
                        """UPDATE productos
                           SET stock = stock - %s
                           WHERE id_producto = %s AND stock >= %s""",
                        (d["cantidad"], d["id_producto"], d["cantidad"]),
                    )
                    if cursor.rowcount == 0:
                        raise ValueError(
                            f"Stock insuficiente para el producto ID {d['id_producto']}"
                        )

            conn.commit()
            return id_venta
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def get_all(search=None):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT v.*, c.nombre AS cliente, COUNT(dv.id_detalle) AS num_items
                    FROM ventas v
                    LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
                    LEFT JOIN detalle_ventas dv ON v.id_venta = dv.id_venta
                """
                params = []
                if search:
                    sql += " WHERE c.nombre LIKE %s OR CAST(v.id_venta AS CHAR) LIKE %s"
                    term = f"%{search}%"
                    params.extend([term, term])
                sql += " GROUP BY v.id_venta ORDER BY v.fecha_venta DESC"
                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_venta):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT v.*, c.nombre AS cliente
                       FROM ventas v
                       LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
                       WHERE v.id_venta = %s""",
                    (id_venta,),
                )
                venta = cursor.fetchone()
                if venta:
                    cursor.execute(
                        """SELECT dv.*, p.nombre AS producto, p.codigo_barras
                           FROM detalle_ventas dv
                           JOIN productos p ON dv.id_producto = p.id_producto
                           WHERE dv.id_venta = %s""",
                        (id_venta,),
                    )
                    venta["detalles"] = cursor.fetchall()
                return venta
        finally:
            conn.close()

    @staticmethod
    def count():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS total FROM ventas")
                return cursor.fetchone()["total"]
        finally:
            conn.close()

    @staticmethod
    def total_ingresos():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COALESCE(SUM(total), 0) AS total FROM ventas")
                return cursor.fetchone()["total"]
        finally:
            conn.close()
