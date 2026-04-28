from flask import Blueprint, render_template, request, redirect, url_for, current_app
from . import get_db_connection
from .analyzer import analyze_sentiment, extract_keywords

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    errors = []
    form_data = {
        "text": "",
        "author": "",
        "rating": "",
    }

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        author = request.form.get("author", "").strip()
        rating_raw = request.form.get("rating", "").strip()

        form_data["text"] = text
        form_data["author"] = author
        form_data["rating"] = rating_raw

        if not text:
            errors.append("Текст отзыва не должен быть пустым.")

        rating = None
        if rating_raw:
            try:
                rating = int(rating_raw)
                if rating < 1 or rating > 5:
                    errors.append("Оценка должна быть от 1 до 5.")
            except ValueError:
                errors.append("Оценка должна быть числом от 1 до 5.")

        if not errors:
            sentiment = analyze_sentiment(text)
            keywords = extract_keywords(text)

            conn = get_db_connection(current_app)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO reviews (text, author, rating, sentiment, keywords) VALUES (?, ?, ?, ?, ?)",
                (text, author or "Аноним", rating, sentiment, keywords),
            )
            conn.commit()
            conn.close()

            return redirect(url_for("main.index"))

    conn = get_db_connection(current_app)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, text, author, rating, sentiment, keywords, created_at "
        "FROM reviews ORDER BY id DESC"
    )
    reviews = cur.fetchall()
    conn.close()

    return render_template(
        "index.html",
        reviews=reviews,
        errors=errors,
        form_data=form_data,
    )