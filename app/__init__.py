from flask import Flask
import os
import sqlite3

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    )

    app.config["DATABASE"] = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "reviews.db"
    )

    from . import routes
    app.register_blueprint(routes.bp)

    @app.cli.command("init-db")
    def init_db_command():
        init_db(app)
        print("Initialized the database.")

    return app


def get_db_connection(app):
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db(app):
    conn = get_db_connection(app)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT,
            rating INTEGER,
            sentiment TEXT NOT NULL DEFAULT 'neutral',
            keywords TEXT,
            created_at TEXT NOT NULL DEFAULT current_timestamp
        )
        """
    )
    conn.commit()
    conn.close()