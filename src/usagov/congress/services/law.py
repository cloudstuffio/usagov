from typing import Any, Dict, Optional
import requests  # type: ignore
from src.usagov.congress.utils import filter_parameters


class LawService:
    SERVICE_PATH = "law"

    def __init__(self, api_key: str, base_url: str) -> None:
        """
        Initialize the LawService.

        Args:
            api_key (str): API key for authenticating with the Congress API.
            base_url (str): The base URL for the Congress API, provided by the Client class.
        """
        self._api_key = api_key
        self.base_url = base_url
        self.format = "json"
        self.headers = {"X-API-Key": self._api_key}
        self.base_endpoint = f"{self.base_url}/{self.SERVICE_PATH}"

    def law(
        self,
        composite_id: Optional[str] = None,
        congress: Optional[int] = None,
        law: Optional[str] = None,
        law_type: str = "public",
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a list of laws or a single law.

        Args:
            composite_id (Optional[str]): The composite ID of the law.
            congress (Optional[int]): The number of the Congress for which to retrieve laws.
            law (Optional[str]): The number of the law to retrieve.
            law_type (str): The type of law to retrieve. Defaults to "public".
                "public" for public law.
                "private" for private law.
            limit (Optional[int]): The maximum number of results to return.
            offset (Optional[int]): The number of results to skip (used for pagination).

        Returns:
            Dict[str, Any]: A dictionary containing the laws data.
        """
        # Define the lookup for the law type parameter
        law_type_lookup = {
            "public": "pub",
            "private": "priv",
        }

        # Construct the query parameters dictionary, only including non-None values
        params = {
            "limit": limit,
            "offset": offset,
        }

        # Remove keys with None values to avoid sending unnecessary parameters
        params = filter_parameters(params)

        if composite_id:
            split_id = composite_id.split("-")
            congress = int(split_id[0])
            law = split_id[1]

        # Construct the endpoint URL
        if congress and law_type and law:
            endpoint = f"{self.base_endpoint}/{congress}/{law_type_lookup.get(law_type.lower())}/{law}"
        elif congress and law_type:
            endpoint = f"{self.base_endpoint}/{congress}/{law_type_lookup.get(law_type.lower())}"
        elif congress:
            endpoint = f"{self.base_endpoint}/{congress}"
        else:
            raise ValueError(
                "The paramater composite_id or congress is required."
            )

        # Send the GET request with the constructed query parameters
        response = requests.get(endpoint, headers=self.headers, params=params)

        # Raise an exception if the response status code indicates an error
        response.raise_for_status()

        # Response JSON
        response_json: Dict[str, Any] = response.json()

        # Return the parsed JSON response
        return response_json
