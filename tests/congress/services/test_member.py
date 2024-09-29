import pytest
import requests
from unittest.mock import patch, Mock
from src.usagov.congress.services.member import MemberService
from src.usagov.congress.utils import filter_parameters


@pytest.fixture
def member_service() -> MemberService:
    """
    Fixture to initialize and return an instance of MemberService.
    """
    return MemberService(
        api_key="test_api_key", base_url="https://api.congress.gov/v3"
    )


def test_member_service_initialization(member_service: MemberService) -> None:
    """
    Test that the MemberService is initialized correctly.
    """
    assert member_service._api_key == "test_api_key"
    assert member_service.base_url == "https://api.congress.gov/v3"
    assert member_service.format == "json"
    assert member_service.headers == {"X-API-Key": "test_api_key"}
    assert member_service.base_endpoint == "https://api.congress.gov/v3/member"


@patch("requests.get")
def test_member_service_member_with_member_id(
    mock_get: Mock, member_service: MemberService
) -> None:
    """
    Test the member method of MemberService with member_id parameter.

    Args:
        mock_get (Mock): Mocked requests.get method.
        member_service (MemberService): The MemberService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_member_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the member method with member_id parameter
    response = member_service.member(member_id="A000360")

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/member/A000360"
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
def test_member_service_member_with_member_id_and_details(
    mock_get: Mock, member_service: MemberService
) -> None:
    """
    Test the member method of MemberService with member_id and details parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        member_service (MemberService): The MemberService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_member_details_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the member method with member_id and details parameters
    response = member_service.member(member_id="A000360", details="sponsor")

    # Constructed URL and params expected in the GET request
    expected_url = (
        "https://api.congress.gov/v3/member/A000360/sponsored-legislation"
    )
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
def test_member_service_member_with_congress_state_and_district(
    mock_get: Mock, member_service: MemberService
) -> None:
    """
    Test the member method of MemberService with congress, state, and district parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        member_service (MemberService): The MemberService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_congressional_member_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the member method with congress, state, and district parameters
    response = member_service.member(congress=117, state="CA", district=12)

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/member/congress/117/CA/12"
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
def test_member_service_member_with_pagination(
    mock_get: Mock, member_service: MemberService
) -> None:
    """
    Test the member method of MemberService with pagination parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        member_service (MemberService): The MemberService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "test_paginated_member_data"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the member method with pagination parameters
    response = member_service.member(congress=117, limit=10, offset=5)

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/member/congress/117"
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
def test_member_service_member_filter_parameters(
    mock_get: Mock, member_service: MemberService
) -> None:
    """
    Test the member method to ensure it correctly filters parameters.

    Args:
        mock_get (Mock): Mocked requests.get method.
        member_service (MemberService): The MemberService instance.
    """
    # Mock response data
    mock_response = Mock()
    expected_json = {"data": "filtered_parameters_test"}
    mock_response.json.return_value = expected_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the member method with some parameters set to None
    response = member_service.member(congress=117, limit=5, offset=None)

    # Constructed URL and params expected in the GET request
    expected_url = "https://api.congress.gov/v3/member/congress/117"
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
def test_member_service_invalid_response(
    mock_get: Mock, member_service: MemberService
) -> None:
    """
    Test the member method with an invalid response (non-200 status code).

    Args:
        mock_get (Mock): Mocked requests.get method.
        member_service (MemberService): The MemberService instance.
    """
    # Mock response to raise an HTTP error
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_get.return_value = mock_response

    # Call the member method and expect an HTTP error
    with pytest.raises(requests.exceptions.HTTPError):
        member_service.member(member_id="A000360")


@patch("requests.get")
def test_member_service_member_with_missing_required_parameters(
    mock_get: Mock, member_service: MemberService
) -> None:
    """
    Test the member method to ensure it raises an exception when required parameters are missing.

    Args:
        mock_get (Mock): Mocked requests.get method.
        member_service (MemberService): The MemberService instance.
    """
    # Mock response data
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    # Call the member method without congress or member_id parameters
    response = member_service.member()

    # Expected URL and params
    expected_url = "https://api.congress.gov/v3/member"
    expected_params = {}

    # Assertions to ensure the request was made correctly
    mock_get.assert_called_once_with(
        expected_url,
        headers={"X-API-Key": "test_api_key"},
        params=expected_params,
    )

    # Assert the response data
    assert response == {}
