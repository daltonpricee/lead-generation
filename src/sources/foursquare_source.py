import logging
from typing import List

from src.config.settings import FOURSQUARE_API_KEY, DEFAULT_LOCATION
from src.models.lead import Lead
from src.utils.http_client import HTTPClient


class FoursquareSource:
    """
    Uses the Foursquare Places API to discover construction companies.

    Filters for smaller businesses based on popularity score.
    """

    SEARCH_URL = "https://api.foursquare.com/v3/places/search"

    def __init__(self, api_key: str | None = None, location: str | None = None) -> None:
        self.api_key: str | None = api_key or FOURSQUARE_API_KEY
        self.location: str | None = location or DEFAULT_LOCATION
        self.http_client: HTTPClient = HTTPClient()

    def search(self, query: str, max_results: int = 200) -> List[Lead]:
        """
        Searches for businesses matching the query.

        Args:
            query: Search term (e.g., "construction company").
            max_results: Maximum number of leads to return.

        Returns:
            List of Lead objects.
        """
        if not self.api_key:
            return self._sample_leads(query)

        headers: dict[str, str] = {
            "Authorization": self.api_key,
            "Accept": "application/json",
        }

        leads: List[Lead] = []
        limit: int = 50  # Foursquare max per request
        offset: int = 0

        while len(leads) < max_results:
            params: dict[str, str | int] = {
                "query": query,
                "near": self.location,
                "limit": min(limit, max_results - len(leads)),
                "offset": offset,
            }

            try:
                response: dict = self.http_client.get_json(self.SEARCH_URL, params=params, headers=headers)
                results: list = response.get("results", [])

                for place in results:
                    name: str | None = place.get("name")
                    if not name:
                        continue

                    # Foursquare popularity score: higher means more popular (avoid very high)
                    popularity: float = place.get("popularity", 0.0)
                    if popularity > 0.9:  # Allow medium-sized companies
                        continue

                    website: str | None = place.get("website")
                    phone: str | None = place.get("tel")
                    address: str = place.get("location", {}).get("formatted_address", "")

                    lead: Lead = Lead(
                        name="",
                        company=name,
                        website=website,
                        email=None,
                        phone=phone,
                        linkedin_url=None,
                        source="Foursquare",
                        industry="Construction",
                    )
                    leads.append(lead)

                if len(results) < limit:
                    break

                offset += limit

            except Exception as exc:
                logging.warning("Foursquare search failed: %s", exc)
                break

        if not leads:
            return self._sample_leads(query)

        return leads[:max_results]

    def _sample_leads(self, query: str) -> List[Lead]:
        """
        Returns sample leads when API is not available.

        Args:
            query: Unused, for consistency.

        Returns:
            List of sample Lead objects.
        """
        companies: list[str] = [
            "Bayfront Builders", "Oceanview Contractors", "Island Renovations",
            "Coastal Construction Co", "Harbor Builders", "Marina Renovations",
            "Lagoon Contractors", "Key Builders", "Shoreline Construction",
            "Reef Renovations", "Cove Contractors", "Inlet Builders",
            "Sound Construction", "Estuary Renovations", "Fjord Contractors",
            "Delta Builders", "Gulf Construction", "Bayou Renovations",
            "Strait Contractors", "Channel Builders", "Peninsula Construction",
            "Isthmus Renovations", "Cape Contractors", "Point Builders",
            "Headland Construction", "Neck Renovations", "Spit Contractors",
            "Tombolo Builders", "Hook Construction", "Bar Renovations",
            "Sandbar Contractors", "Dune Builders", "Beach Construction",
            "Dune Renovations", "Shore Contractors", "Coast Builders",
            "Seaside Construction", "Littoral Renovations", "Riparian Contractors",
            "Fluvial Builders", "Riverine Construction", "Lacustrine Renovations",
            "Palustrine Contractors", "Bog Builders", "Marsh Construction",
            "Swamp Renovations", "Fen Contractors", "Moor Builders",
            "Heath Construction", "Moorland Renovations", "Downland Contractors"
        ]
        leads: List[Lead] = []
        for i, company in enumerate(companies[:50]):
            leads.append(Lead(
                name=f"Contact {i+1}",
                company=company,
                website=f"https://foursquare.com/v/{company.lower().replace(' ', '-')}",
                email=None,
                phone=None,
                linkedin_url=None,
                source="Foursquare (sample)",
                industry="Construction",
            ))
        return leads