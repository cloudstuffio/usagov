import pytest
import requests
from unittest.mock import patch, Mock
from src.usagov.congress.services.law import LawService


@pytest.fixture
def law_service() -> LawService:
    """
    Fixture to initialize and return an instance of LawService.
    """
    return LawService(
        api_key="test_api_key", base_url="https://api.congress.gov/v3"
    )


def test_law_service_initialization(law_service: LawService) -> None:
    """
    Test that the LawService is initialized correctly.
    """
    assert law_service._api_key == "test_api_key"
    assert law_service.base_url == "https://api.congress.gov/v3"
    assert law_service.format == "json"
    assert law_service.headers == {"X-API-Key": "test_api_key"}
    assert law_service.base_endpoint == "https://api.congress.gov/v3/law"


@patch("requests.get")
def test_law_service_law_with_composite_id_and_law_type(
    mock_get: Mock, law_service: LawService
) -> None:
    """
    Test the law method of LawService with a composite ID and separate law_type parameter.

    Args:
        mock_get (Mock): Mocked requests.get method.
        law_service (LawService): The LawService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the law method with a composite ID and law_type parameter
    response = law_service.law(composite_id="117-123", law_type="public")

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/law/117/pub/123"
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
def test_law_service_law_with_congress_and_law_type(
    mock_get: Mock, law_service: LawService
) -> None:
    """
    Test the law method of LawService with congress and law_type parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        law_service (LawService): The LawService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_law_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the law method with congress and law_type parameters
    response = law_service.law(congress=117, law="123", law_type="public")

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/law/117/pub/123"
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
def test_law_service_law_with_congress_and_law(
    mock_get: Mock, law_service: LawService
) -> None:
    """
    Test the law method of LawService with congress and law parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        law_service (LawService): The LawService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_law_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the law method with specific congress and law parameters
    response = law_service.law(congress=117, law="123", law_type="public")

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/law/117/pub/123"
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
def test_law_service_law_with_pagination(
    mock_get: Mock, law_service: LawService
) -> None:
    """
    Test the law method of LawService with pagination parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        law_service (LawService): The LawService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "paginated_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the law method with pagination parameters
    response = law_service.law(
        congress=117, law_type="public", limit=10, offset=5
    )

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/law/117/pub"
    expected_params = {"limit": 10, "offset": 5}

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == expected_json


@patch("requests.get")
def test_law_service_law_filter_parameters(
    mock_get: Mock, law_service: LawService
) -> None:
    """
    Test the law method to ensure it correctly filters parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        law_service (LawService): The LawService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "filtered_parameters_test"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the law method with some parameters set to None
    response = law_service.law(
        congress=117, law_type="public", limit=5, offset=None
    )

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/law/117/pub"
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
def test_law_service_invalid_response(
    mock_get: Mock, law_service: LawService
) -> None:
    """
    Test the law method with an invalid response (non-200 status code).

    Args:
        mock_get (Mock): Mocked requests.get method.
        law_service (LawService): The LawService instance.
    """
    # Mock response to raise an HTTP error
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_get.return_value = mock_response

    # Call the law method and expect an HTTP error
    with pytest.raises(requests.exceptions.HTTPError):
        law_service.law(congress=117, law_type="public")


@patch("requests.get")
def test_law_service_law_with_missing_required_parameters(
    mock_get: Mock, law_service: LawService
) -> None:
    """
    Test the law method to ensure it raises a ValueError when required parameters are missing.

    Args:
        mock_get (Mock): Mocked requests.get method.
        law_service (LawService): The LawService instance.
    """
    # Ensure ValueError is raised when required parameters are missing
    with pytest.raises(
        ValueError, match="The paramater composite_id or congress is required."
    ):
        law_service.law(limit=5)
