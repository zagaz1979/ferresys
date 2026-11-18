# FerreSys 🔧

Sistema de gestión de inventario y ventas para ferretería, desarrollado con **Python + Flask + MySQL** bajo arquitectura **MVC**.

## Requisitos

- Python 3.11+
- MySQL 8.0+
- [uv](https://docs.astral.sh/uv/) (Astral)

## Instalación

```bash
# 1. Clonar / descomprimir el proyecto
cd ferresys

# 2. Sincronizar dependencias con uv
uv sync

# 3. Crear la base de datos
mysql -u root -p < sql/schema.sql

# 4. Configurar variables de entorno (opcional)
cp .env.example .env
# editar .env con tus credenciales

# 5. Ejecutar
uv run python app.py
Abrir en el navegador: http://127.0.0.1:5000
