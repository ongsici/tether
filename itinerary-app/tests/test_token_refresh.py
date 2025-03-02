import pytest
from unittest.mock import patch, MagicMock
import src.utils.api_refresh_token as token_module
from src.utils.api_refresh_token import get_amadeus_token, get_valid_token


@pytest.fixture(autouse=True)
def reset_token_globals():
    """
    A fixture that runs before (and after) each test, ensuring
    token_module.token and token_module.token_expiry are reset to
    None and 0. This prevents one test's state from leaking into another.
    """
    token_module.token = None
    token_module.token_expiry = 0
    yield
    token_module.token = None
    token_module.token_expiry = 0


@patch("src.utils.api_refresh_token.requests.post")
def test_get_amadeus_token_successfully_fetches_token(mock_post):
    """
    GIVEN a valid response (status_code=200) from Amadeus OAuth
    WHEN get_amadeus_token is called
    THEN it should parse the JSON, set the global token, and return it.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "access_token": "test_access_token",
        "expires_in": 3600
    }
    mock_post.return_value = mock_response

    returned_token = get_amadeus_token()
    assert returned_token == "test_access_token"
    mock_post.assert_called_once()

    assert token_module.token == "test_access_token"
    assert token_module.token_expiry > 0


@patch("src.utils.api_refresh_token.requests.post")
def test_get_amadeus_token_raises_exception_on_error(mock_post):
    """
    GIVEN an invalid response that triggers raise_for_status()
    WHEN get_amadeus_token is called
    THEN it should raise an Exception.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("Invalid credentials")
    mock_post.return_value = mock_response
    
    with pytest.raises(Exception) as exc_info:
        get_amadeus_token()
    assert "Invalid credentials" in str(exc_info.value)
    mock_post.assert_called_once()


@patch("src.utils.api_refresh_token.time.time", return_value=1000)
@patch("src.utils.api_refresh_token.get_amadeus_token")
def test_get_valid_token_fetches_new_token_if_no_token(mock_get_token, mock_time):
    """
    GIVEN token=None initially
    WHEN get_valid_token() is called
    THEN it should fetch a new token (calling get_amadeus_token) exactly once.
    """
    mock_get_token.return_value = "new_token_value"

    result = get_valid_token()
    assert result == "new_token_value"
    mock_get_token.assert_called_once()


@patch("src.utils.api_refresh_token.get_amadeus_token")
def test_get_valid_token_fetches_new_token_after_expiration(mock_get_token):
    """
    GIVEN a token is fetched at time=1000 but it expires before time=2000,
    WHEN we call get_valid_token() at time=2000,
    THEN it should call get_amadeus_token() again for a new token.
    """
    with patch("src.utils.api_refresh_token.time.time", return_value=1000):
        mock_get_token.return_value = "first_token"
        result1 = get_valid_token()
        assert result1 == "first_token"
        assert mock_get_token.call_count == 1

    with patch("src.utils.api_refresh_token.time.time", return_value=2000):
        mock_get_token.return_value = "second_token"
        result2 = get_valid_token()
        assert result2 == "second_token"
        assert mock_get_token.call_count == 2


@patch("src.utils.api_refresh_token.get_amadeus_token")
def test_get_valid_token_propagates_exception_if_refresh_fails(mock_get_token):
    """
    GIVEN an expired token
    WHEN a refresh attempt is made (calling get_amadeus_token),
    AND that call raises an Exception,
    THEN the exception should bubble up to the caller.
    """

    with patch("src.utils.api_refresh_token.time.time", return_value=1000):
        mock_get_token.return_value = "initial_token"
        first = get_valid_token()
        assert first == "initial_token"
        assert mock_get_token.call_count == 1

    mock_get_token.side_effect = Exception("Network error")
    with patch("src.utils.api_refresh_token.time.time", return_value=2000):
        with pytest.raises(Exception) as exc:
            get_valid_token()
        assert "Network error" in str(exc.value)
        assert mock_get_token.call_count == 2
