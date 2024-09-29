from typing import Any, Dict, Optional
import requests  # type: ignore
from src.usagov.congress.utils import filter_parameters


class TreatyService:
    SERVICE_PATH = "treaty"

    def __init__(self, api_key: str, base_url: str) -> None:
        """
        Initialize the TreatyService.

        Args:
            api_key (str): API key for authenticating with the Congress API.
            base_url (str): The base URL for the Congress API, provided by the Client class.
        """
        self._api_key = api_key
        self.base_url = base_url
        self.format = "json"
        self.headers = {"X-API-Key": self._api_key}
        self.base_endpoint = f"{self.base_url}/{self.SERVICE_PATH}"

    def treaty(
        self,
        congress: Optional[int] = None,
        details: Optional[str] = None,
        from_datetime: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        to_datetime: Optional[str] = None,
        treaty: Optional[int] = None,
        treaty_part: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a list of treaties or a single treaty.

        Args:
            congress (Optional[int]): The number of the Congress for which to retrieve treaties.
            details (Optional[str]): The detail to include in the response.
            from_datetime (Optional[str]): The start date for filtering treaties.
            limit (Optional[int]): The maximum number of results to return.
            offset (Optional[int]): The number of results to skip.
            to_datetime (Optional[str]): The end date for filtering treaties.
            treaty (Optional[int]): The number of the treaty to retrieve.
            treaty_part (Optional[str]): The part of the treaty to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing the treaties data.
        """
        # Define the lookup for the details parameter
        details_lookup = {
            "actions": "actions",
            "committees": "committees",
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

        # Construct the endpoint URL
        if congress and treaty and treaty_part and details:
            endpoint = f"{self.base_endpoint}/{congress}/{treaty}/{treaty_part}/{details_lookup.get(details)}"
        elif congress and treaty and treaty_part:
            endpoint = f"{self.base_endpoint}/{congress}/{treaty}/{treaty_part}"
        elif congress and treaty and details:
            endpoint = f"{self.base_endpoint}/{congress}/{treaty}/{details_lookup.get(details)}"
        elif congress and treaty:
            endpoint = f"{self.base_endpoint}/{congress}/{treaty}"
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
