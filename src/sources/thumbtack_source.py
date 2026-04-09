import logging
from typing import List

from src.config.settings import THUMBTACK_API_KEY, DEFAULT_LOCATION
from src.models.lead import Lead
from src.utils.http_client import HTTPClient


class ThumbtackSource:
    """
    Attempts to load construction bookkeeping leads from Thumbtack.

    If a Thumbtack API key is not configured, the class returns a fallback set
    of sample construction leads that can be replaced with a real Thumbtack API
    integration later.
    """

    BASE_URL = "https://www.thumbtack.com/services/api/v1/search"

    def __init__(self, api_key: str | None = None, location: str | None = None):
        self.api_key = api_key or THUMBTACK_API_KEY
        self.location = location or DEFAULT_LOCATION
        self.http_client = HTTPClient()

    def search(self, query: str, max_results: int = 20) -> List[Lead]:
        if not self.api_key:
            return self._sample_leads(query)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        params = {
            "query": query,
            "location": self.location,
            "limit": max_results,
        }

        try:
            results = self.http_client.get_json(self.BASE_URL, params=params, headers=headers)
            leads = []

            for item in results.get("data", [])[:max_results]:
                company_name = item.get("businessName") or item.get("title")
                if not company_name:
                    continue

                website = item.get("websiteUrl") or item.get("url")
                phone = item.get("phone") or item.get("displayPhone")
                industry = "Construction"

                lead = Lead(
                    name=item.get("contactName", ""),
                    company=company_name,
                    website=website,
                    email=None,
                    phone=phone,
                    linkedin_url=item.get("linkedinUrl"),
                    source="Thumbtack",
                    industry=industry,
                )
                leads.append(lead)

            if not leads:
                return self._sample_leads(query)

            return leads

        except Exception as exc:
            logging.warning("Thumbtack search failed: %s", exc)
            return self._sample_leads(query)

    def _sample_leads(self, query: str) -> List[Lead]:
        return [
            Lead(
                name="Ariel Gonzalez",
                company="Phoenix Construction Co",
                website="https://phoenixconstructionco.com",
                email=None,
                phone=None,
                linkedin_url=None,
                source="Thumbtack (sample)",
                industry="Construction",
            ),
            Lead(
                name="Janet Carter",
                company="Ridge Line Builders",
                website="https://ridgelinebuilders.com",
                email=None,
                phone=None,
                linkedin_url=None,
                source="Thumbtack (sample)",
                industry="Construction",
            ),
        ]
