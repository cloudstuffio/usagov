import pytest
import requests
from unittest.mock import patch, Mock
from src.usagov.congress.services.congress import CongressService
from src.usagov.congress.utils import filter_parameters


@pytest.fixture
def congress_service() -> CongressService:
    """
    Fixture to initialize and return an instance of CongressService.
    """
    return CongressService(
        api_key="test_api_key", base_url="https://api.congress.gov/v3"
    )


def test_congress_service_initialization(
    congress_service: CongressService,
) -> None:
    """
    Test that the CongressService is initialized correctly.
    """
    assert congress_service._api_key == "test_api_key"
    assert congress_service.base_url == "https://api.congress.gov/v3"
    assert congress_service.format == "json"
    assert congress_service.headers == {"X-API-Key": "test_api_key"}
    assert (
        congress_service.base_endpoint == "https://api.congress.gov/v3/congress"
    )


@patch("requests.get")
def test_congress_service_congress_with_congress_param(
    mock_get: Mock, congress_service: CongressService
) -> None:
    """
    Test the congress method of CongressService with a specific congress number.

    Args:
        mock_get (Mock): Mocked requests.get method.
        congress_service (CongressService): The CongressService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the congress method with a specific congress number
    response = congress_service.congress(congress=117)

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/congress/117"
    expected_params = {}

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == expected_json


@patch("requests.get")
def test_congress_service_congress_with_current_congress(
    mock_get: Mock, congress_service: CongressService
) -> None:
    """
    Test the congress method of CongressService with the current_congress parameter set to True.

    Args:
        mock_get (Mock): Mocked requests.get method.
        congress_service (CongressService): The CongressService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_current_congress"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the congress method with current_congress=True
    response = congress_service.congress(current_congress=True)

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/congress/current"
    expected_params = {}

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == expected_json


@patch("requests.get")
def test_congress_service_congress_with_pagination(
    mock_get: Mock, congress_service: CongressService
) -> None:
    """
    Test the congress method of CongressService with pagination parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        congress_service (CongressService): The CongressService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_paginated_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the congress method with pagination parameters
    response = congress_service.congress(limit=10, offset=20)

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/congress"
    expected_params = {"limit": 10, "offset": 20}

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == expected_json


@patch("requests.get")
def test_congress_service_congress_filter_parameters(
    mock_get: Mock, congress_service: CongressService
) -> None:
    """
    Test the congress method to ensure it correctly filters parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        congress_service (CongressService): The CongressService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "filtered_parameters_test"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the congress method with some parameters set to None
    response = congress_service.congress(limit=5, offset=None)

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/congress"
    expected_params = {"limit": 5}  # None values should be filtered out

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == expected_json


@patch("requests.get")
def test_congress_service_congress_invalid_response(
    mock_get: Mock, congress_service: CongressService
) -> None:
    """
    Test the congress method with an invalid response (non-200 status code).

    Args:
        mock_get (Mock): Mocked requests.get method.
        congress_service (CongressService): The CongressService instance.
    """
    # Mock response to raise an HTTP error
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_get.return_value = mock_response

    # Call the congress method and expect an HTTP error
    with pytest.raises(requests.exceptions.HTTPError):
        congress_service.congress(congress=117)
