import pytest
from src.usagov.congress.client import Client
from src.usagov.congress.services.amendment import AmendmentService
from src.usagov.congress.services.bill import BillService
from src.usagov.congress.services.congress import CongressService
from src.usagov.congress.services.hearing import HearingService
from src.usagov.congress.services.law import LawService
from src.usagov.congress.services.member import MemberService
from src.usagov.congress.services.summary import SummaryService
from src.usagov.congress.services.treaty import TreatyService
from typing import Iterator


@pytest.fixture
def client() -> Iterator[Client]:
    """
    Fixture that initializes and returns an instance of the Client class for testing.

    Yields:
        Client: An instance of the Client class with a test API key and base URL.
    """
    yield Client(api_key="test_api_key", base_url="https://api.congress.gov/v3")


def test_client_initialization(client: Client) -> None:
    """
    Test to verify the Client initialization.

    Args:
        client (Client): The Client instance initialized with the fixture.
    """
    assert client.api_key == "test_api_key"
    assert client.base_url == "https://api.congress.gov/v3"


def test_amendment_service(client: Client) -> None:
    """
    Test to verify the AmendmentService instantiation.

    Args:
        client (Client): The Client instance initialized with the fixture.
    """
    service: AmendmentService = client.amendment()
    assert isinstance(service, AmendmentService)
    assert service._api_key == "test_api_key"
    assert service.base_url == "https://api.congress.gov/v3"


def test_bill_service(client: Client) -> None:
    service: BillService = client.bill()
    assert isinstance(service, BillService)
    assert service._api_key == "test_api_key"
    assert service.base_url == "https://api.congress.gov/v3"


def test_congress_service(client: Client) -> None:
    service: CongressService = client.congress()
    assert isinstance(service, CongressService)
    assert service._api_key == "test_api_key"
    assert service.base_url == "https://api.congress.gov/v3"


def test_hearing_service(client: Client) -> None:
    service: HearingService = client.hearing()
    assert isinstance(service, HearingService)
    assert service._api_key == "test_api_key"
    assert service.base_url == "https://api.congress.gov/v3"


def test_law_service(client: Client) -> None:
    service: LawService = client.law()
    assert isinstance(service, LawService)
    assert service._api_key == "test_api_key"
    assert service.base_url == "https://api.congress.gov/v3"


def test_member_service(client: Client) -> None:
    service: MemberService = client.member()
    assert isinstance(service, MemberService)
    assert service._api_key == "test_api_key"
    assert service.base_url == "https://api.congress.gov/v3"


def test_summary_service(client: Client) -> None:
    service: SummaryService = client.summary()
    assert isinstance(service, SummaryService)
    assert service._api_key == "test_api_key"
    assert service.base_url == "https://api.congress.gov/v3"


def test_treaty_service(client: Client) -> None:
    service: TreatyService = client.treaty()
    assert isinstance(service, TreatyService)
    assert service._api_key == "test_api_key"
    assert service.base_url == "https://api.congress.gov/v3"
