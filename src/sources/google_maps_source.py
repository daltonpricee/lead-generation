from typing import List

from src.config.settings import GOOGLE_MAPS_API_KEY, DEFAULT_LOCATION
from src.models.lead import Lead
from src.utils.http_client import HTTPClient


class GoogleMapsSource:
    """
    Uses the Google Maps Places API to discover small construction companies.

    If the API key is not configured, it falls back to sample data.
    """

    PLACE_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

    def __init__(self, api_key: str | None = None, location: str | None = None):
        self.api_key = api_key or GOOGLE_MAPS_API_KEY
        self.location = location or DEFAULT_LOCATION
        self.http_client = HTTPClient()

    def search(self, query: str, max_results: int = 100) -> List[Lead]:
        if not self.api_key:
            return self._sample_leads(query)

        all_leads: List[Lead] = []
        next_page_token = None

        while len(all_leads) < max_results:
            payload = {
                "query": f"{query} near {self.location}",
                "key": self.api_key,
            }
            if next_page_token:
                payload["pagetoken"] = next_page_token

            response = self.http_client.get_json(self.PLACE_SEARCH_URL, params=payload)
            results = response.get("results", [])
            next_page_token = response.get("next_page_token")

            for place in results:
                if len(all_leads) >= max_results:
                    break
                company = place.get("name")
                if not company:
                    continue

                user_ratings = place.get("user_ratings_total", 0)
                if user_ratings and user_ratings > 300:
                    continue

                website, phone = self._fetch_place_details(place.get("place_id"))
                all_leads.append(
                    Lead(
                        name="",
                        company=company,
                        website=website,
                        email=None,
                        phone=phone,
                        linkedin_url=None,
                        source="Google Maps",
                        industry="Construction",
                    )
                )

            if not next_page_token:
                break

            # Wait a bit for next page token to become valid
            import time
            time.sleep(2)

        if not all_leads:
            return self._sample_leads(query)

        return all_leads

    def _fetch_place_details(self, place_id: str | None) -> tuple[str | None, str | None]:
        if not place_id:
            return None, None

        payload = {
            "place_id": place_id,
            "fields": "website,formatted_phone_number",
            "key": self.api_key,
        }

        response = self.http_client.get_json(self.PLACE_DETAILS_URL, params=payload)
        result = response.get("result", {})
        return result.get("website"), result.get("formatted_phone_number")

    def _sample_leads(self, query: str) -> List[Lead]:
        return [
            Lead(
                name="Ethan Wells",
                company="Sunset Construction Services",
                website="https://sunsetconstructionservices.com",
                email=None,
                phone=None,
                linkedin_url=None,
                source="Google Maps (sample)",
                industry="Construction",
            ),
            Lead(
                name="Nina Alvarez",
                company="Pinnacle Builders",
                website="https://pinnaclebuildersfl.com",
                email=None,
                phone=None,
                linkedin_url=None,
                source="Google Maps (sample)",
                industry="Construction",
            ),
            Lead(
                name="Carlos Ramirez",
                company="Miami Home Renovations",
                website="https://mihomesreno.com",
                email=None,
                phone=None,
                linkedin_url=None,
                source="Google Maps (sample)",
                industry="Construction",
            ),
            Lead(
                name="Sofia Lopez",
                company="Palm Beach Contractors",
                website="https://palmbeachcontractors.com",
                email=None,
                phone=None,
                linkedin_url=None,
                source="Google Maps (sample)",
                industry="Construction",
            ),
        ]