import re
from typing import Optional

from src.utils.http_client import HTTPClient


class WebsiteCollector:
    """
    Collects contact information from public company web pages.
    """

    EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    PHONE_REGEX = r"\+?\d[\d\s\-]{7,15}"

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    def extract_email(self, html: str) -> Optional[str]:
        """
        Extracts the first email found in HTML.

        Args:
            html (str): Raw HTML content.

        Returns:
            Optional[str]: Email if found, else None.
        """
        match = re.search(self.EMAIL_REGEX, html)
        return match.group(0) if match else None

    def extract_phone(self, html: str) -> Optional[str]:
        """
        Extracts the first phone number found in HTML.

        Args:
            html (str): Raw HTML content.

        Returns:
            Optional[str]: Phone number if found, else None.
        """
        match = re.search(self.PHONE_REGEX, html)
        return match.group(0) if match else None

    # def scrape_contact_info(self, website: str) -> dict:
    #     """
    #     Scrapes contact info from a website.

    #     Args:
    #         website (str): Website URL.

    #     Returns:
    #         dict: Extracted contact info (email, phone).
    #     """
    #     html = self.http_client.get(website)

    #     return {
    #         "email": self.extract_email(html),
    #         "phone": self.extract_phone(html),
    #     }

    def scrape_contact_info(self, website: str) -> dict:
        """
        Demo enrichment: generates realistic contact info.

        Args:
            website (str): Website URL.

        Returns:
            dict: Fake but believable contact info.
        """
        domain = website.replace("https://", "").replace("www.", "")

        return {
            "email": f"info@{domain}",
            "phone": "602-555-1234"
        }