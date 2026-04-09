import requests


class HTTPClient:
    """
    Simple HTTP client wrapper for making requests.
    """

    def get(self, url: str, timeout: int = 10) -> str:
        """
        Sends a GET request.

        Args:
            url (str): Target URL.
            timeout (int): Request timeout in seconds.

        Returns:
            str: Response text.

        Raises:
            requests.RequestException: If request fails.
        """
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text

    def get_json(self, url: str, params: dict | None = None, headers: dict | None = None, timeout: int = 10) -> dict:
        """
        Sends a GET request and returns JSON.

        Args:
            url (str): Target URL.
            params (dict | None): Query parameters.
            headers (dict | None): Request headers.
            timeout (int): Request timeout in seconds.

        Returns:
            dict: Parsed JSON response.
        """
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()