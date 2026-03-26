from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint("main", __name__)

reviews = []

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        author = request.form.get("author", "").strip()

        if text:
            reviews.append(
                {
                    "text": text,
                    "author": author or "Аноним",
                }
            )
        return redirect(url_for("main.index"))

    return render_template("index.html", reviews=reviews)