import pytest
import responses
from main import get_news_by_keyword, get_top_news
from keys import news_api

@pytest.mark.parametrize("keyword, expected_articles", [
    ("keyword", [
        {
            "source":{
                "id":"some-id1",
                "name":"Some Name 1"
            },
            "author":"Somebody 1",
            "title": "Article 1",
            "description": "Description 1",
            "url": "https://somesite1.com/article1"
        },
        {
            "source":{
                "id":"some-id2",
                "name":"Some Name 2"
            },
            "author":"Somebody 2",
            "title": "Article 2",
            "description": "Description 2",
            "url": "https://somesite2.com/article2"
        }
    ]),
])

@responses.activate
def test_get_news_by_keyword(keyword, expected_articles):
    responses.add(
        responses.GET,
        f"https://newsapi.org/v2/everything?q=keyword&language=en&apiKey={news_api}",
        status="ok",
        json={"articles": expected_articles}
    )

    articles = get_news_by_keyword(keyword)

    assert len(articles) == len(expected_articles)
    assert articles == expected_articles

@pytest.mark.parametrize("expected_articles", [
    [
        {
            "source":{
                "id":"some-id1",
                "name":"Some Name 1"
            },
            "author":"Somebody 1",
            "title": "Top article 1",
            "description": "Top description 1",
            "url": "https://somesite1.com/top-article1"
        },
        {
            "source":{
                "id":"some-id2",
                "name":"Some Name 2"
            },
            "author":"Somebody 2",
            "title": "Top article 2",
            "description": "Top description 2",
            "url": "https://somesite2.com/top-article2"
        }
    ]
])

@responses.activate
def test_get_top_news(expected_articles):
    responses.add(
        responses.GET,
        f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}",
        status="ok",
        json={"articles": expected_articles}
    )

    articles = get_top_news()

    assert len(articles) == len(expected_articles)
    assert articles == expected_articles