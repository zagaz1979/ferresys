from config import get_db_connection


class CategoriaModel:

    @staticmethod
    def get_all(search=None):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM categorias"
                params = []
                if search:
                    sql += " WHERE nombre LIKE %s OR descripcion LIKE %s"
                    term = f"%{search}%"
                    params.extend([term, term])
                sql += " ORDER BY nombre ASC"
                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_categoria):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM categorias WHERE id_categoria = %s",
                    (id_categoria,),
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
                    "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)",
                    (data["nombre"], data.get("descripcion")),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def update(id_categoria, data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE categorias SET nombre=%s, descripcion=%s WHERE id_categoria=%s",
                    (data["nombre"], data.get("descripcion"), id_categoria),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def delete(id_categoria):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM categorias WHERE id_categoria = %s",
                    (id_categoria,),
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
                cursor.execute("SELECT COUNT(*) AS total FROM categorias")
                return cursor.fetchone()["total"]
        finally:
            conn.close()
