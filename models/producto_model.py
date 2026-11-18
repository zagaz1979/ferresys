from config import get_db_connection


class ProductoModel:

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT p.*, c.nombre AS categoria
                    FROM productos p
                    LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
                    ORDER BY p.nombre ASC
                    """
                )
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_producto):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM productos WHERE id_producto = %s",
                    (id_producto,),
                )
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def create(data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO productos
                       (codigo_barras, nombre, precio_compra, precio_venta,
                        stock, stock_minimo, id_categoria)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                        data["codigo_barras"],
                        data["nombre"],
                        data["precio_compra"],
                        data["precio_venta"],
                        data["stock"],
                        data["stock_minimo"],
                        data["id_categoria"],
                    ),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def update(id_producto, data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """UPDATE productos
                       SET codigo_barras=%s, nombre=%s, precio_compra=%s,
                           precio_venta=%s, stock=%s, stock_minimo=%s, id_categoria=%s
                       WHERE id_producto=%s""",
                    (
                        data["codigo_barras"],
                        data["nombre"],
                        data["precio_compra"],
                        data["precio_venta"],
                        data["stock"],
                        data["stock_minimo"],
                        data["id_categoria"],
                        id_producto,
                    ),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def delete(id_producto):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM productos WHERE id_producto = %s", (id_producto,)
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def count():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS total FROM productos")
                return cursor.fetchone()["total"]
        finally:
            conn.close()

    @staticmethod
    def count_stock_bajo():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) AS total FROM productos WHERE stock <= stock_minimo"
                )
                return cursor.fetchone()["total"]
        finally:
            conn.close()

    @staticmethod
    def valor_inventario():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COALESCE(SUM(stock * precio_compra), 0) AS total FROM productos"
                )
                return cursor.fetchone()["total"]
        finally:
            conn.close()
