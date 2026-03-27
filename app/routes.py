from flask import Blueprint, render_template, request, redirect, url_for, current_app
from . import get_db_connection

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        author = request.form.get("author", "").strip()

        if text:
            conn = get_db_connection(current_app)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO reviews (text, author) VALUES (?, ?)",
                (text, author or "Аноним"),
            )
            conn.commit()
            conn.close()

        return redirect(url_for("main.index"))

    conn = get_db_connection(current_app)
    cur = conn.cursor()
    cur.execute("SELECT id, text, author FROM reviews ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    return render_template("index.html", reviews=rows)