from app.analyzer import analyze_sentiment, extract_keywords


def test_analyze_sentiment_positive():
    text = "Отличный и удобный сервис, всё очень понравилось"
    result = analyze_sentiment(text)

    assert result == "positive"


def test_analyze_sentiment_negative():
    text = "Ужасный и медленный сервис, сплошная проблема"
    result = analyze_sentiment(text)

    assert result == "negative"


def test_analyze_sentiment_neutral():
    text = "Сегодня была доставка заказа"
    result = analyze_sentiment(text)

    assert result == "neutral"


def test_extract_keywords_returns_string():
    text = "Быстрая доставка и хорошее качество товара"
    result = extract_keywords(text)

    assert isinstance(result, str)
    assert result != ""


def test_extract_keywords_contains_expected_words():
    text = "Быстрая доставка и хорошее качество товара"
    result = extract_keywords(text)

    assert "доставка" in result
    assert "качество" in result


def test_extract_keywords_respects_limit():
    text = "Хороший удобный быстрый сервис и качественный товар с отличной доставкой"
    result = extract_keywords(text, limit=3)

    keywords = [item.strip() for item in result.split(",") if item.strip()]
    assert len(keywords) <= 3


def test_extract_keywords_removes_duplicates():
    text = "Хороший товар, хороший сервис, хороший магазин"
    result = extract_keywords(text)

    keywords = [item.strip() for item in result.split(",") if item.strip()]
    assert len(keywords) == len(set(keywords))