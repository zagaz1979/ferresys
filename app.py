from flask import Flask, render_template
from config import Config

from controllers.producto_controller import producto_bp
from controllers.categoria_controller import categoria_bp
from controllers.cliente_controller import cliente_bp
from controllers.venta_controller import venta_bp

from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registrar blueprints
    app.register_blueprint(producto_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(venta_bp)

     # Context processor: inyecta el año actual en todas las plantillas
    @app.context_processor
    def inject_current_year():
        return {"current_year": datetime.now().year}

    @app.route("/")
    def home():
        return render_template("index.html")

    # Manejo global de errores
    @app.errorhandler(404)
    def not_found(e):
        return render_template("base.html", error="Recurso no encontrado (404)"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("base.html", error="Error interno del servidor (500)"), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
