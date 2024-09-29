import pytest
import requests
from unittest.mock import patch, Mock
from src.usagov.congress.services.treaty import TreatyService
from src.usagov.congress.utils import filter_parameters


@pytest.fixture
def treaty_service() -> TreatyService:
    """
    Fixture to initialize and return an instance of TreatyService.
    """
    return TreatyService(
        api_key="test_api_key", base_url="https://api.congress.gov/v3"
    )


def test_treaty_service_initialization(treaty_service: TreatyService) -> None:
    """
    Test that the TreatyService is initialized correctly.
    """
    assert treaty_service._api_key == "test_api_key"
    assert treaty_service.base_url == "https://api.congress.gov/v3"
    assert treaty_service.format == "json"
    assert treaty_service.headers == {"X-API-Key": "test_api_key"}
    assert treaty_service.base_endpoint == "https://api.congress.gov/v3/treaty"


@patch("requests.get")
def test_treaty_service_treaty_with_congress_and_treaty_number(
    mock_get: Mock, treaty_service: TreatyService
) -> None:
    """
    Test the treaty method of TreatyService with congress and treaty parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        treaty_service (TreatyService): The TreatyService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_treaty_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the treaty method with congress and treaty parameters
    response = treaty_service.treaty(congress=117, treaty=456)

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/treaty/117/456"
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
def test_treaty_service_treaty_with_details(
    mock_get: Mock, treaty_service: TreatyService
) -> None:
    """
    Test the treaty method of TreatyService with congress, treaty, and details parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        treaty_service (TreatyService): The TreatyService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_treaty_details_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the treaty method with congress, treaty, and details parameters
    response = treaty_service.treaty(
        congress=117, treaty=456, details="actions"
    )

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/treaty/117/456/actions"
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
def test_treaty_service_treaty_with_treaty_part(
    mock_get: Mock, treaty_service: TreatyService
) -> None:
    """
    Test the treaty method of TreatyService with congress, treaty, and treaty_part parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        treaty_service (TreatyService): The TreatyService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_treaty_part_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the treaty method with congress, treaty, and treaty_part parameters
    response = treaty_service.treaty(congress=117, treaty=456, treaty_part="A")

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/treaty/117/456/A"
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
def test_treaty_service_treaty_with_pagination(
    mock_get: Mock, treaty_service: TreatyService
) -> None:
    """
    Test the treaty method of TreatyService with pagination parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        treaty_service (TreatyService): The TreatyService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "paginated_treaty_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the treaty method with pagination parameters
    response = treaty_service.treaty(congress=117, limit=5, offset=10)

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/treaty/117"
    expected_params = {"limit": 5, "offset": 10}

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == expected_json


@patch("requests.get")
def test_treaty_service_treaty_filter_parameters(
    mock_get: Mock, treaty_service: TreatyService
) -> None:
    """
    Test the treaty method to ensure it correctly filters parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        treaty_service (TreatyService): The TreatyService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "filtered_parameters_test"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the treaty method with some parameters set to None
    response = treaty_service.treaty(congress=117, limit=5, offset=None)

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/treaty/117"
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
def test_treaty_service_invalid_response(
    mock_get: Mock, treaty_service: TreatyService
) -> None:
    """
    Test the treaty method with an invalid response (non-200 status code).

    Args:
        mock_get (Mock): Mocked requests.get method.
        treaty_service (TreatyService): The TreatyService instance.
    """
    # Mock response to raise an HTTP error
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_get.return_value = mock_response

    # Call the treaty method and expect an HTTP error
    with pytest.raises(requests.exceptions.HTTPError):
        treaty_service.treaty(congress=117)


@patch("requests.get")
def test_treaty_service_treaty_with_missing_required_parameters(
    mock_get: Mock, treaty_service: TreatyService
) -> None:
    """
    Test the treaty method to ensure it raises an exception when required parameters are missing.

    Args:
        mock_get (Mock): Mocked requests.get method.
        treaty_service (TreatyService): The TreatyService instance.
    """
    # Mock response data
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    # Call the treaty method without congress or treaty parameters
    response = treaty_service.treaty()

    # Expected URL and params
    expected_url = "https://api.congress.gov/v3/treaty"
    expected_params = {}

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == {}
