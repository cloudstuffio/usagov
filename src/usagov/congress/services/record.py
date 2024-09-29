from typing import Any, Dict, Optional
import requests  # type: ignore
from src.usagov.congress.utils import filter_parameters


# TODO
class RecordService:
    # SERVICE_PATH = "member"

    def __init__(self, api_key: str, base_url: str) -> None:
        """
        Initialize the RecordService.

        Args:
            api_key (str): API key for authenticating with the Congress API.
            base_url (str): The base URL for the Congress API, provided by the Client class.
        """
        self._api_key = api_key
        self.base_url = base_url
        self.format = "json"
        self.headers = {"X-API-Key": self._api_key}
        # self.base_endpoint = f"{self.base_url}/{self.SERVICE_PATH}"
