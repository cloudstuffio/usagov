from typing import Any, Dict, Optional
import requests  # type: ignore
from src.usagov.congress.utils import filter_parameters


class BillService:
    SERVICE_PATH = "bill"

    def __init__(self, api_key: str, base_url: str) -> None:
        """
        Initialize the BillService.

        Args:
            api_key (str): API key for authenticating with the Congress API.
            base_url (str): The base URL for the Congress API, provided by the Client class.
        """
        self._api_key = api_key
        self.base_url = base_url
        self.format = "json"
        self.headers = {"X-API-Key": self._api_key}
        self.base_endpoint = f"{self.base_url}/{self.SERVICE_PATH}"

    def bill(
        self,
        bill: Optional[str] = None,
        bill_type: Optional[str] = None,
        composite_id: Optional[str] = None,
        congress: Optional[int] = None,
        details: Optional[str] = None,
        from_datetime: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        to_datetime: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a list of bills or a single bill.

        Args:
            bill (Optional[str]): The number of the bill to retrieve.
            bill_type (Optional[str]): The type of bill to retrieve.
                hr: House Bill
                s: Senate Bill
                hjres: House Joint Resolution
                sjres: Senate Joint Resolution
                hconres: House Concurrent Resolution
                sconres: Senate Concurrent Resolution
                hres: House Resolution
                sres: Senate Resolution
            composite_id (Optional[str]): The composite ID of the bill.
            congress (Optional[int]): The number of the Congress for which to retrieve bills.
            details (Optional[str]): The detail to include in the response.
            from_datetime (Optional[str]): The start date for filtering bills.
            limit (Optional[int]): The maximum number of results to return.
            offset (Optional[int]): The number of results to skip.
            sort (Optional[str]): The order in which to sort results.
            to_datetime (Optional[str]): The end date for filtering bills.

        Returns:
            Dict[str, Any]: A dictionary containing the bills data.
        """
        # Define the lookup for the details parameter
        details_lookup = {
            "actions": "actions",
            "amendments": "amendments",
            "committees": "committees",
            "cosponsors": "cosponsors",
            "related": "relatedbills",
            "subjects": "subjects",
            "summaries": "summaries",
            "text": "text",
            "titles": "titles",
        }

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

        if composite_id:
            split_id = composite_id.split("-")
            congress = int(split_id[0])
            bill_type = split_id[1]
            bill = split_id[2]

        # Construct the endpoint URL
        if congress and bill_type and bill and details:
            endpoint = f"{self.base_endpoint}/{congress}/{bill_type}/{bill}/{details_lookup.get(details)}"
        elif congress and bill_type and bill:
            endpoint = f"{self.base_endpoint}/{congress}/{bill_type}/{bill}"
        elif congress and bill_type:
            endpoint = f"{self.base_endpoint}/{congress}/{bill_type}"
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
