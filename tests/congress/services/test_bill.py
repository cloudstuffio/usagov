import pytest
import requests
from unittest.mock import patch, Mock
from src.usagov.congress.services.bill import BillService
from src.usagov.congress.utils import filter_parameters


# Define a fixture for BillService
@pytest.fixture
def bill_service() -> BillService:
    """
    Fixture to initialize and return an instance of BillService.
    """
    return BillService(
        api_key="test_api_key", base_url="https://api.congress.gov/v3"
    )


def test_bill_service_initialization(bill_service: BillService) -> None:
    """
    Test that the BillService is initialized correctly.
    """
    assert bill_service._api_key == "test_api_key"
    assert bill_service.base_url == "https://api.congress.gov/v3"
    assert bill_service.format == "json"
    assert bill_service.headers == {"X-API-Key": "test_api_key"}
    assert bill_service.base_endpoint == "https://api.congress.gov/v3/bill"


@patch("requests.get")
def test_bill_service_bill(mock_get: Mock, bill_service: BillService) -> None:
    """
    Test the bill method of BillService.

    Args:
        mock_get (Mock): Mocked requests.get method.
        bill_service (BillService): The BillService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the bill method with specific parameters
    response = bill_service.bill(
        bill="123",
        bill_type="hr",
        congress=117,
        details="actions",
        limit=5,
        sort="asc",
    )

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/bill/117/hr/123/actions"
    expected_params = {"limit": 5, "sort": "asc"}

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == expected_json


@patch("requests.get")
def test_bill_service_bill_composite_id(
    mock_get: Mock, bill_service: BillService
) -> None:
    """
    Test the bill method of BillService using composite_id.

    Args:
        mock_get (Mock): Mocked requests.get method.
        bill_service (BillService): The BillService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the bill method with a composite ID
    response = bill_service.bill(
        composite_id="117-hr-123", details="summaries", limit=10
    )

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/bill/117/hr/123/summaries"
    expected_params = {"limit": 10}

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == expected_json


@patch("requests.get")
def test_bill_service_empty_response(
    mock_get: Mock, bill_service: BillService
) -> None:
    """
    Test the bill method with an empty response.

    Args:
        mock_get (Mock): Mocked requests.get method.
        bill_service (BillService): The BillService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the bill method without any specific parameters
    response = bill_service.bill()

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/bill"
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
def test_bill_service_invalid_response(
    mock_get: Mock, bill_service: BillService
) -> None:
    """
    Test the bill method with an invalid response (non-200 status code).

    Args:
        mock_get (Mock): Mocked requests.get method.
        bill_service (BillService): The BillService instance.
    """
    # Mock response to raise an HTTP error
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_get.return_value = mock_response

    # Call the bill method and expect an HTTP error
    with pytest.raises(requests.exceptions.HTTPError):
        bill_service.bill(bill="123", bill_type="hr", congress=117)


@patch("requests.get")
def test_bill_service_bill_filter_parameters(
    mock_get: Mock, bill_service: BillService
) -> None:
    """
    Test the bill method to ensure it correctly filters parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        bill_service (BillService): The BillService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "filtered_parameters_test"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the bill method with parameters, including some None values
    response = bill_service.bill(
        bill="123",
        bill_type="hr",
        congress=117,
        limit=10,
        from_datetime=None,
        to_datetime=None,
        sort=None,
    )

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/bill/117/hr/123"
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
