import spacy

nlp = spacy.load("ru_core_news_sm")

POSITIVE_WORDS = {
    "хороший",
    "отличный",
    "супер",
    "классный",
    "прекрасный",
    "удобный",
    "быстрый",
    "любить",
    "нравиться",
    "замечательный",
    "идеальный",
    "понравиться",
    "радовать",
}

NEGATIVE_WORDS = {
    "плохой",
    "ужасный",
    "медленный",
    "неудобный",
    "ненавидеть",
    "проблема",
    "ошибка",
    "сломаться",
    "отвратительный",
    "кошмар",
    "глючный",
    "разочаровать",
    "долгий",
}


def analyze_sentiment(text):
    doc = nlp(text.lower())
    positive_count = 0
    negative_count = 0

    for token in doc:
        if token.is_space or token.is_punct:
            continue

        lemma = token.lemma_.lower()

        if lemma in POSITIVE_WORDS:
            positive_count += 1

        if lemma in NEGATIVE_WORDS:
            negative_count += 1

    if positive_count > negative_count:
        return "positive"

    if negative_count > positive_count:
        return "negative"

    return "neutral"