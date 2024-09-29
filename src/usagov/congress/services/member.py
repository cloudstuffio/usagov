from typing import Any, Dict, Optional
import requests  # type: ignore
from src.usagov.congress.utils import filter_parameters


class MemberService:
    SERVICE_PATH = "member"

    def __init__(self, api_key: str, base_url: str) -> None:
        """
        Initialize the MemberService.

        Args:
            api_key (str): API key for authenticating with the Congress API.
            base_url (str): The base URL for the Congress API, provided by the Client class.
        """
        self._api_key = api_key
        self.base_url = base_url
        self.format = "json"
        self.headers = {"X-API-Key": self._api_key}
        self.base_endpoint = f"{self.base_url}/{self.SERVICE_PATH}"

    def member(
        self,
        congress: Optional[int] = None,
        current_member: Optional[bool] = None,
        details: Optional[str] = None,
        district: Optional[int] = None,
        from_datetime: Optional[str] = None,
        limit: Optional[int] = None,
        member_id: Optional[str] = None,
        offset: Optional[int] = None,
        state: Optional[str] = None,
        to_datetime: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a list of congressional members or a single member.

        Args:
            congress (Optional[int]): The number of the Congress for which to retrieve members.
            current_member (Optional[bool]): Whether to retrieve only current members.
            details (Optional[str]): The detail to include in the response.
            district (Optional[int]): The district number to retrieve.
            from_datetime (Optional[str]): The start date for filtering members.
            limit (Optional[int]): The maximum number of results to return.
            member_id (Optional[str]): The ID of the member to retrieve.
            offset (Optional[int]): The number of results to skip.
            state (Optional[str]): The state (two letter abbreviation) to retrieve.
            to_datetime (Optional[str]): The end date for filtering members.

        Returns:
            Dict[str, Any]: A dictionary containing the congressional member data.
        """
        # Define the lookup for the details parameter
        details_lookup = {
            "cosponsor": "cosponsored-legislation",
            "sponsor": "sponsored-legislation",
        }

        # Construct the query parameters dictionary, only including non-None values
        params = {
            "currentMember": current_member,
            "fromDateTime": from_datetime,
            "limit": limit,
            "offset": offset,
            "toDateTime": to_datetime,
        }

        # Remove keys with None values to avoid sending unnecessary parameters
        params = filter_parameters(params)

        # Construct the endpoint URL
        if member_id and details:
            endpoint = f"{self.base_endpoint}/{member_id}/{details_lookup.get(details)}"
        elif member_id:
            endpoint = f"{self.base_endpoint}/{member_id}"
        elif congress and state and district:
            endpoint = (
                f"{self.base_endpoint}/congress/{congress}/{state}/{district}"
            )
        elif congress:
            endpoint = f"{self.base_endpoint}/congress/{congress}"
        elif state and district:
            endpoint = f"{self.base_endpoint}/{state}/{district}"
        elif state:
            endpoint = f"{self.base_endpoint}/{state}"
        else:
            endpoint = f"{self.base_endpoint}"

        # Send the GET request with the constructed query parameters
        response = requests.get(endpoint, headers=self.headers, params=params)

        # Raise an exception if the response status code indicates an error
        response.raise_for_status()

        # Response JSON
        response_json: Dict[str, Any] = response.json()

        # Return the parsed JSON response
        return response_json
