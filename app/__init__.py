from flask import Flask
import os

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates")
    )

    from . import routes
    app.register_blueprint(routes.bp)

    return app