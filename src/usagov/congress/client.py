from src.usagov.congress.services.amendment import AmendmentService
from src.usagov.congress.services.bill import BillService
from src.usagov.congress.services.congress import CongressService
from src.usagov.congress.services.hearing import HearingService
from src.usagov.congress.services.law import LawService
from src.usagov.congress.services.member import MemberService
from src.usagov.congress.services.summary import SummaryService
from src.usagov.congress.services.treaty import TreatyService


class Client:
    def __init__(
        self, api_key: str, base_url: str = "https://api.congress.gov/v3"
    ) -> None:
        """
        Initialize the Congress API Client.

        Args:
            api_key (str): API key for authenticating with the Congress API.
            base_url (str): The base URL for the Congress API.
        """
        self.api_key = api_key
        self.base_url = base_url

    def amendment(self) -> AmendmentService:
        """
        Return an instance of the AmendmentsService class.

        Returns:
            AmendmentsService: An instance of the AmendmentsService class.
        """
        return AmendmentService(self.api_key, self.base_url)

    def bill(self) -> BillService:
        """
        Return an instance of the BillsService class.

        Returns:
            BillsService: An instance of the BillsService class.
        """
        return BillService(self.api_key, self.base_url)

    def congress(self) -> CongressService:
        """
        Return an instance of the CongressService class.

        Returns:
            CongressService: An instance of the CongressService class.
        """
        return CongressService(self.api_key, self.base_url)

    def hearing(self) -> HearingService:
        """
        Return an instance of the HearingsService class.

        Returns:
            HearingsService: An instance of the HearingsService class.
        """
        return HearingService(self.api_key, self.base_url)

    def law(self) -> LawService:
        """
        Return an instance of the LawsService class.

        Returns:
            LawsService: An instance of the LawsService class.
        """
        return LawService(self.api_key, self.base_url)

    def member(self) -> MemberService:
        """
        Return an instance of the MembersService class.

        Returns:
            MembersService: An instance of the MembersService class.
        """
        return MemberService(self.api_key, self.base_url)

    def summary(self) -> SummaryService:
        """
        Return an instance of the SummaryService class.

        Returns:
            SummaryService: An instance of the SummaryService class.
        """
        return SummaryService(self.api_key, self.base_url)

    def treaty(self) -> TreatyService:
        """
        Return an instance of the TreatiesService class.

        Returns:
            TreatiesService: An instance of the TreatiesService class.
        """
        return TreatyService(self.api_key, self.base_url)
