from flask import Blueprint, render_template, request, redirect, url_for, current_app
from . import get_db_connection

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        author = request.form.get("author", "").strip()
        rating_raw = request.form.get("rating", "").strip()

        if text:
            try:
                rating = int(rating_raw) if rating_raw else None
            except ValueError:
                rating = None

            conn = get_db_connection(current_app)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO reviews (text, author, rating) VALUES (?, ?, ?)",
                (text, author or "Аноним", rating),
            )
            conn.commit()
            conn.close()

        return redirect(url_for("main.index"))

    conn = get_db_connection(current_app)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, text, author, rating, created_at "
        "FROM reviews ORDER BY id DESC"
    )
    reviews = cur.fetchall()
    conn.close()

    return render_template("index.html", reviews=reviews)