import logging
from typing import List

from src.config.settings import YELP_API_KEY, DEFAULT_LOCATION
from src.models.lead import Lead
from src.utils.http_client import HTTPClient


class YelpSource:
    """
    Uses the Yelp Fusion API to discover small construction companies.

    If the API key is not configured, it falls back to sample data.
    """

    SEARCH_URL = "https://api.yelp.com/v3/businesses/search"

    def __init__(self, api_key: str | None = None, location: str | None = None):
        self.api_key = api_key or YELP_API_KEY
        self.location = location or DEFAULT_LOCATION
        self.http_client = HTTPClient()

    def search(self, query: str, max_results: int = 200) -> List[Lead]:
        if not self.api_key:
            return self._sample_leads(query)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

        leads: List[Lead] = []
        limit = 50  # Yelp max per request
        offset = 0

        while len(leads) < max_results and offset < 1000:  # Yelp offset limit
            params = {
                "term": query,
                "location": self.location,
                "limit": min(limit, max_results - len(leads)),
                "offset": offset,
                "sort_by": "rating",  # To get higher rated, but we filter later
            }

            try:
                response = self.http_client.get_json(self.SEARCH_URL, params=params, headers=headers)
                businesses = response.get("businesses", [])

                for biz in businesses:
                    name = biz.get("name")
                    if not name:
                        continue

                    review_count = biz.get("review_count", 0)
                    if review_count > 500:  # Allow medium-sized companies
                        continue

                    website = biz.get("url")  # Yelp page, not business website
                    phone = biz.get("display_phone")
                    address = biz.get("location", {}).get("address1", "")

                    lead = Lead(
                        name="",
                        company=name,
                        website=website,
                        email=None,
                        phone=phone,
                        linkedin_url=None,
                        source="Yelp",
                        industry="Construction",
                    )
                    leads.append(lead)

                if len(businesses) < limit:
                    break  # No more results

                offset += limit

            except Exception as exc:
                logging.warning("Yelp search failed: %s", exc)
                break

        if not leads:
            return self._sample_leads(query)

        return leads[:max_results]

    def _sample_leads(self, query: str) -> List[Lead]:
        import random
        companies = [
            "Everglades Construction", "Coral Gables Builders", "Brickell Renovations",
            "Wynwood Contractors", "Little Havana Builders", "Doral Renovations",
            "Kendall Construction", "Homestead Builders", "Cutler Bay Contractors",
            "Pinecrest Renovations", "South Miami Builders", "Gables Contractors",
            "Bal Harbour Renovations", "Surfside Builders", "Sunny Isles Construction",
            "Aventura Contractors", "Hallandale Renovations", "Hollywood Builders",
            "Pembroke Pines Contractors", "Miramar Renovations", "Davie Builders",
            "Cooper City Construction", "Weston Contractors", "Plantation Builders",
            "Sunrise Renovations", "Lauderhill Construction", "Tamarac Contractors",
            "Coral Springs Builders", "Parkland Renovations", "Margate Construction",
            "Coconut Creek Contractors", "Deerfield Beach Builders", "Boca Raton Renovations",
            "Delray Beach Construction", "Boynton Beach Contractors", "Lake Worth Builders",
            "West Palm Beach Renovations", "Palm Beach Gardens Construction", "Jupiter Contractors",
            "Stuart Builders", "Port St. Lucie Renovations", "Fort Pierce Construction",
            "Stuart Contractors", "Port St. Lucie Builders", "Fort Pierce Renovations"
        ]
        leads = []
        for i, company in enumerate(companies[:50]):
            leads.append(Lead(
                name=f"Contact {i+1}",
                company=company,
                website=f"https://yelp.com/biz/{company.lower().replace(' ', '-')}",
                email=None,
                phone=None,
                linkedin_url=None,
                source="Yelp (sample)",
                industry="Construction",
            ))
        return leads