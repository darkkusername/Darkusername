from src.trends import analyze

def test_international_english_scoring():
    result = analyze([{"topic":"AI agent automation","recency_signal":90}])
    assert len(result) == 1
    assert result[0]["priority"] in {"NOW","NEXT","WATCH"}
    assert result[0]["international_relevance"] >= 80

def test_algeria_is_not_a_trend_criterion():
    result = analyze([{"topic":"Algeria AI trend"},{"topic":"AI agents"}])
    assert len(result) == 1
    assert result[0]["topic"] == "AI agents"
