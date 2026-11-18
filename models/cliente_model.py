from config import get_db_connection


class ClienteModel:

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM clientes ORDER BY nombre ASC")
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_cliente):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM clientes WHERE id_cliente = %s",
                    (id_cliente,),
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
                    """INSERT INTO clientes (nombre, telefono, email, direccion)
                       VALUES (%s, %s, %s, %s)""",
                    (
                        data["nombre"],
                        data.get("telefono"),
                        data.get("email"),
                        data.get("direccion"),
                    ),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def update(id_cliente, data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """UPDATE clientes SET nombre=%s, telefono=%s, email=%s, direccion=%s
                       WHERE id_cliente=%s""",
                    (
                        data["nombre"],
                        data.get("telefono"),
                        data.get("email"),
                        data.get("direccion"),
                        id_cliente,
                    ),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def delete(id_cliente):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,)
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
                cursor.execute("SELECT COUNT(*) AS total FROM clientes")
                return cursor.fetchone()["total"]
        finally:
            conn.close()
