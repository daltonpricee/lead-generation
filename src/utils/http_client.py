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