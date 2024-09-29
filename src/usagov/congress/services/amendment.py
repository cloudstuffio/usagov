from typing import Any, Dict, Optional
import requests  # type: ignore
from src.usagov.congress.utils import filter_parameters


class AmendmentService:
    SERVICE_PATH = "amendment"

    def __init__(self, api_key: str, base_url: str) -> None:
        """
        Initialize the AmendmentService.

        Args:
            api_key (str): API key for authenticating with the Congress API.
            base_url (str): The base URL for the Congress API, provided by the Client class.
        """
        self._api_key = api_key
        self.base_url = base_url
        self.format = "json"
        self.headers = {"X-API-Key": self._api_key}
        self.base_endpoint = f"{self.base_url}/{self.SERVICE_PATH}"

    def amendment(
        self,
        amendment_number: Optional[str] = None,
        amendment_type: Optional[str] = None,
        composite_id: Optional[str] = None,
        congress: Optional[int] = None,
        details: Optional[str] = None,
        from_datetime: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        to_datetime: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a list of amendments or a single amendment.

        Args:
            amendment_number (Optional[str]): The number of the amendment to retrieve.
            amendment_type (Optional[str]): The type of amendment to retrieve.
            composite_id (Optional[str]): The composite ID of the amendment.
            congress (Optional[int]): The number of the Congress for which to retrieve amendments.
            details (Optional[str]): The detail to include in the response.
            from_datetime (Optional[str]): The start date for filtering amendments.
            limit (Optional[int]): The maximum number of results to return.
            offset (Optional[int]): The number of results to skip.
            to_datetime (Optional[str]): The end date for filtering amendments.

        Returns:
            Dict[str, Any]: A dictionary containing the amendments data.
        """
        # Define the lookup for the details parameter
        details_lookup = {
            "actions": "actions",
            "amendments": "amendments",
            "cosponsors": "cosponsors",
            "text": "text",
        }

        # Construct the query parameters dictionary, only including non-None values
        params = {
            "fromDateTime": from_datetime,
            "limit": limit,
            "offset": offset,
            "toDateTime": to_datetime,
        }

        # Remove keys with None values to avoid sending unnecessary parameters
        params = filter_parameters(params)

        if composite_id:
            split_id = composite_id.split("-")
            congress = int(split_id[0])
            amendment_type = split_id[1]
            amendment_number = split_id[2]

        # Construct the endpoint URL
        if congress and amendment_type and amendment_number and details:
            endpoint = f"{self.base_endpoint}/{congress}/{amendment_type}/{amendment_number}/{details_lookup.get(details)}"
        elif congress and amendment_type and amendment_number:
            endpoint = f"{self.base_endpoint}/{congress}/{amendment_type}/{amendment_number}"
        elif congress and amendment_type:
            endpoint = f"{self.base_endpoint}/{congress}/{amendment_type}"
        elif congress:
            endpoint = f"{self.base_endpoint}/{congress}"
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
