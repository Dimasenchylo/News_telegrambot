import pytest
import responses
from response import get_response
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
def test_get_response_everything(keyword, expected_articles):
    responses.add(
        responses.GET,
        f"https://newsapi.org/v2/everything?q={keyword}&language=en&apiKey={news_api}",
        status="ok",
        json={"articles": expected_articles}
    )

    articles = get_response('everything', keyword)

    assert len(articles) == len(expected_articles)
    assert articles == expected_articles

@pytest.mark.parametrize("expected_articles", [
    ([
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
def test_get_response_top(expected_articles):
    responses.add(
        responses.GET,
        f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}",
        status="ok",
        json={"articles": expected_articles}
    )

    articles = get_response('top')

    assert len(articles) == len(expected_articles)
    assert articles == expected_articles

@pytest.mark.parametrize("category, expected_articles", [
    ("business", [
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
def test_get_response_category(category, expected_articles):
    responses.add(
        responses.GET,
        f"https://newsapi.org/v2/top-headlines?category={category}&country=us&apiKey={news_api}",
        status="ok",
        json={"articles": expected_articles}
    )

    articles = get_response('category', category)

    assert len(articles) == len(expected_articles)
    assert articles == expected_articles
