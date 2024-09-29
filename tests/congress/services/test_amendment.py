import pytest
import requests
from unittest.mock import patch, Mock
from src.usagov.congress.services.amendment import AmendmentService
from src.usagov.congress.utils import filter_parameters


# Define a fixture for AmendmentService
@pytest.fixture
def amendment_service() -> AmendmentService:
    """
    Fixture to initialize and return an instance of AmendmentService.
    """
    return AmendmentService(
        api_key="test_api_key", base_url="https://api.congress.gov/v3"
    )


def test_amendment_service_initialization(
    amendment_service: AmendmentService,
) -> None:
    """
    Test that the AmendmentService is initialized correctly.
    """
    assert amendment_service._api_key == "test_api_key"
    assert amendment_service.base_url == "https://api.congress.gov/v3"
    assert amendment_service.format == "json"
    assert amendment_service.headers == {"X-API-Key": "test_api_key"}
    assert (
        amendment_service.base_endpoint
        == "https://api.congress.gov/v3/amendment"
    )


@patch("requests.get")
def test_amendment_service_amendment(
    mock_get: Mock, amendment_service: AmendmentService
) -> None:
    """
    Test the amendment method of AmendmentService with specific parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        amendment_service (AmendmentService): The AmendmentService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the amendment method with specific parameters
    response = amendment_service.amendment(
        amendment_number="123",
        amendment_type="hamdt",
        congress=117,
        details="actions",
        limit=5,
    )

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/amendment/117/hamdt/123/actions"
    expected_params = {"limit": 5}

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == expected_json


@patch("requests.get")
def test_amendment_service_amendment_composite_id(
    mock_get: Mock, amendment_service: AmendmentService
) -> None:
    """
    Test the amendment method of AmendmentService using composite_id.

    Args:
        mock_get (Mock): Mocked requests.get method.
        amendment_service (AmendmentService): The AmendmentService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the amendment method with a composite ID
    response = amendment_service.amendment(
        composite_id="117-hamdt-123", details="text", offset=10
    )

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/amendment/117/hamdt/123/text"
    expected_params = {"offset": 10}

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == expected_json


@patch("requests.get")
def test_amendment_service_amendment_empty_response(
    mock_get: Mock, amendment_service: AmendmentService
) -> None:
    """
    Test the amendment method with an empty response.

    Args:
        mock_get (Mock): Mocked requests.get method.
        amendment_service (AmendmentService): The AmendmentService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the amendment method without any specific parameters
    response = amendment_service.amendment()

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/amendment"
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
def test_amendment_service_amendment_filter_parameters(
    mock_get: Mock, amendment_service: AmendmentService
) -> None:
    """
    Test the amendment method to ensure it correctly filters parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        amendment_service (AmendmentService): The AmendmentService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "filtered_parameters_test"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the amendment method with parameters, including some None values
    response = amendment_service.amendment(
        amendment_number="123",
        amendment_type="hamdt",
        congress=117,
        limit=10,
        from_datetime=None,
        to_datetime=None,
    )

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/amendment/117/hamdt/123"
    expected_params = {"limit": 10}  # None values should be filtered out

    # Print the actual call arguments for debugging
    print(f"Actual call args: {mock_get.call_args}")

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == expected_json


@patch("requests.get")
def test_amendment_service_invalid_response(
    mock_get: Mock, amendment_service: AmendmentService
) -> None:
    """
    Test the amendment method with an invalid response (non-200 status code).

    Args:
        mock_get (Mock): Mocked requests.get method.
        amendment_service (AmendmentService): The AmendmentService instance.
    """
    # Mock response to raise an HTTP error
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_get.return_value = mock_response

    # Call the amendment method and expect an HTTP error
    with pytest.raises(requests.exceptions.HTTPError):
        amendment_service.amendment(
            amendment_number="123", amendment_type="hamdt", congress=117
        )
