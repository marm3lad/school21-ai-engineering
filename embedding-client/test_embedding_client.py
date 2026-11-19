from unittest.mock import patch, MagicMock
from embedding_client import get_embedding
import pytest
import requests

def make_response(code, embedding=None):
    fake_response = MagicMock()
    fake_response.status_code = code
    fake_response.json.return_value = embedding

    return fake_response

def test_200():
    fake_response = make_response(200, {"embedding": [0.1, 0.2, 0.3]})

    with patch("embedding_client.requests.post", return_value=fake_response) as mock_post:
        result = get_embedding("привет")

    assert result == [0.1, 0.2, 0.3]
    assert mock_post.call_count == 1

def test_500_200():
    fake_500 = make_response(500)
    fake_200 = make_response(200, {"embedding": [0.1, 0.2, 0.3]})
    with patch("embedding_client.requests.post", side_effect=[fake_500, fake_200]) as mock_post, \
        patch("embedding_client.time.sleep") as mock_sleep:
        result = get_embedding("привет")

    assert result == [0.1, 0.2, 0.3]
    assert mock_post.call_count == 2
    assert mock_sleep.call_count == 1

def test_404():
    fake_404 = make_response(404)
    with patch("embedding_client.requests.post", return_value=fake_404) as mock_post, \
        patch("embedding_client.time.sleep") as mock_sleep:
        with pytest.raises(Exception, match="404"):
            get_embedding("привет")

    assert mock_post.call_count == 1
    assert mock_sleep.call_count == 0

def test_timeout():
    fake_200 = make_response(200, {"embedding": [0.1, 0.2, 0.3]})
    with patch("embedding_client.requests.post", side_effect=[requests.exceptions.Timeout(), fake_200]) as mock_post, \
        patch("embedding_client.time.sleep") as mock_sleep:
        result = get_embedding("привет")

    assert result == [0.1, 0.2, 0.3]
    assert mock_post.call_count == 2
    assert mock_sleep.call_count == 1

def test_no_retries():
    fake_500 = make_response(500)
    with patch("embedding_client.requests.post", return_value=fake_500) as mock_post, \
        patch("embedding_client.time.sleep") as mock_sleep:
        with pytest.raises(Exception, match="все попытки исчерпаны"):
            get_embedding("привет", {"max_retries": 0, "delay": 1, "multiplier": 2})

    assert mock_post.call_count == 1
    assert mock_sleep.call_count == 0