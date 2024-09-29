from typing import Any, Dict, Optional
import requests  # type: ignore
from src.usagov.congress.utils import filter_parameters


class CongressService:
    SERVICE_PATH = "congress"

    def __init__(self, api_key: str, base_url: str) -> None:
        """
        Initialize the CongressService.

        Args:
            api_key (str): API key for authenticating with the Congress API.
            base_url (str): The base URL for the Congress API, provided by the Client class.
        """
        self._api_key = api_key
        self.base_url = base_url
        self.format = "json"
        self.headers = {"X-API-Key": self._api_key}
        self.base_endpoint = f"{self.base_url}/{self.SERVICE_PATH}"

    def congress(
        self,
        congress: Optional[int] = None,
        current_congress: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a list of Congresses or a single Congress.

        Args:
            congress (Optional[int]): The number of the Congress to retrieve.
            current_congress (Optional[bool]): Whether to retrieve the current Congress.
            limit (Optional[int]): The maximum number of results to return.
            offset (Optional[int]): The number of results to skip.

        Returns:
            Dict[str, Any]: A dictionary containing the congresses data.
        """
        # Construct the query parameters dictionary, only including non-None values
        params = {
            "limit": limit,
            "offset": offset,
        }

        # Remove keys with None values to avoid sending unnecessary parameters
        params = filter_parameters(params)

        # Construct the endpoint URL
        if current_congress:
            endpoint = f"{self.base_endpoint}/current"
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
