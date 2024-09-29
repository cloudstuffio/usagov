from typing import Any, Dict, Optional
import requests  # type: ignore
from src.usagov.congress.utils import filter_parameters


class SummaryService:
    SERVICE_PATH = "summaries"

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

    def summary(
        self,
        bill_type: Optional[str] = None,
        congress: Optional[int] = None,
        from_datetime: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        to_datetime: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a list of summaries or a single summary.

        Args:
            congress (Optional[int]): The number of the Congress for which to retrieve summaries.
            bill_type (Optional[str]): The type of bill to retrieve.
                hr: House Bill
                s: Senate Bill
                hjres: House Joint Resolution
                sjres: Senate Joint Resolution
                hconres: House Concurrent Resolution
                sconres: Senate Concurrent Resolution
                hres: House Resolution
                sres: Senate Resolution
            from_datetime (Optional[str]): The start date for filtering amendments.
            limit (Optional[int]): The maximum number of results to return.
            offset (Optional[int]): The number of results to skip.
            sort (Optional[str]): The order in which to sort results.
            to_datetime (Optional[str]): The end date for filtering amendments.

        Returns:
            Dict[str, Any]: A dictionary containing the congressional member data.
        """
        # Construct the query parameters dictionary, only including non-None values
        params = {
            "fromDateTime": from_datetime,
            "limit": limit,
            "offset": offset,
            "sort": sort,
            "toDateTime": to_datetime,
        }

        # Remove keys with None values to avoid sending unnecessary parameters
        params = filter_parameters(params)

        print(params)

        # Construct the endpoint URL
        if congress and bill_type:
            endpoint = f"{self.base_endpoint}/{congress}/{bill_type}"
            print(endpoint)
        elif congress:
            endpoint = f"{self.base_endpoint}/{congress}"
            print(endpoint)
        else:
            endpoint = f"{self.base_endpoint}"
            print(endpoint)

        # Send the GET request with the constructed query parameters
        response = requests.get(endpoint, headers=self.headers, params=params)

        # Raise an exception if the response status code indicates an error
        response.raise_for_status()

        # Response JSON
        response_json: Dict[str, Any] = response.json()

        print(len(response_json.get("summaries")))

        # Return the parsed JSON response
        return response_json
