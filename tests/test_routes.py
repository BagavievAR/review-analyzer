from app import get_db_connection


def test_index_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    page = response.get_data(as_text=True)

    assert "Review Analyzer" in page
    assert "Добавить отзыв" in page
    assert "Список отзывов" in page


def test_index_page_shows_empty_state(client):
    response = client.get("/")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Отзывы не найдены" in page
    assert "Попробуйте изменить фильтры или добавить новый отзыв." in page


def test_submit_valid_review(client):
    response = client.post(
        "/",
        data={
            "text": "Очень хороший сервис, всё понравилось",
            "author": "Alice",
            "rating": "5",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    page = response.get_data(as_text=True)

    assert "Alice" in page
    assert "Очень хороший сервис, всё понравилось" in page
    assert "Оценка: 5/5" in page


def test_submit_review_uses_default_author_when_empty(client):
    response = client.post(
        "/",
        data={
            "text": "Текст без автора",
            "author": "",
            "rating": "4",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    page = response.get_data(as_text=True)

    assert "Аноним" in page
    assert "Текст без автора" in page
    assert "Оценка: 4/5" in page


def test_submit_empty_text_does_not_create_review(app, client):
    response = client.post(
        "/",
        data={
            "text": "   ",
            "author": "Bob",
            "rating": "3",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():
        conn = get_db_connection(app)
        row = conn.execute("SELECT COUNT(*) AS count FROM reviews").fetchone()
        conn.close()

    assert row["count"] == 0


def test_invalid_rating_does_not_create_review(app, client):
    response = client.post(
        "/",
        data={
            "text": "Отзыв с некорректной оценкой",
            "author": "Kate",
            "rating": "abc",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():
        conn = get_db_connection(app)
        row = conn.execute(
            "SELECT text, author, rating FROM reviews WHERE author = ?",
            ("Kate",),
        ).fetchone()
        conn.close()

    assert row is None


def test_review_is_saved_to_database(app, client):
    client.post(
        "/",
        data={
            "text": "Нормальный отзыв",
            "author": "Ivan",
            "rating": "4",
        },
        follow_redirects=True,
    )

    with app.app_context():
        conn = get_db_connection(app)
        row = conn.execute(
            "SELECT text, author, rating FROM reviews WHERE author = ?",
            ("Ivan",),
        ).fetchone()
        conn.close()

    assert row is not None
    assert row["text"] == "Нормальный отзыв"
    assert row["author"] == "Ivan"
    assert row["rating"] == 4